import requests
from common import *
from bs4 import BeautifulSoup
import re

async def lyrics(ctx):
    args = ctx.content.split(" ", 1)
    regex = r"\"([^\"]*)\""

    if len(args) < 2:
        return await client.send_message(ctx.channel, "@{}, please enter both the song name and the artist name, enclosed in quotes(\"\")".format(ctx.author))
    result = re.findall(regex, args[1])

    if len(result) < 2:
        return await client.send_message(ctx.channel, "@{}, please enter both the song name and the artist name, enclosed in quotes(\"\")".format(ctx.author))
    elif len(result) > 2:
        return await client.send_message(ctx.channel, "@{}, please only enter the song name and the artist name, enclosed in quotes(\"\")".format(ctx.author))
    else:
        title = result[0]
        artist_name = result[1]

        if (title == "" or title == " ") or (artist_name == "" or artist_name == " "):
            return await client.send_message(ctx.channel, "@{}, please don't leave the quotes empty (you're not getting anything out of this)".format(ctx.author))

    search_url = auth["genius_auth"]["base_api_url"] + "/search?q=" + title
    data = {'q' : title}

    header = {"Authorization" : (auth["genius_auth"]["headers"]["Authorization"] + auth["genius_auth"]["token"])}
    response = requests.get(search_url, data = data, headers = header)
    json_rp = response.json()
    song_info = None

    if "error" in json_rp:
        return await client.send_message(ctx.channel, "AN ERROR OCCURRED: Please refrain from using this command until this bug is fixed")

    if str(json_rp["meta"]["status"]).startswith(('4', '5')) :
        return await client.send_message(ctx.channel, "Error: " + json_rp["meta"]["message"])

    for hit in json_rp["response"]["hits"]:
        if artist_name in hit["result"]["primary_artist"]["name"]:
            song_info = hit
            break

    if song_info is not None:
        full_song_url = auth["genius_auth"]["base_song_url"] + song_info["result"]["path"]
        song_page = requests.get(full_song_url)
        html = BeautifulSoup(song_page.text, "html.parser")
        [h.extract() for h in html('script')]
        lyrics = html.find("div", class_="lyrics").get_text()
        lyrics_arr = lyrics.split("\n")

        arr_idx = 0
        total_length = 0
        lyrics_line_split = ""

        for l in lyrics_arr:
            # print("Line: " + l)
            total_length += len(l)
            # print("Total Length: " + str(total_length))
            if total_length >= 1700:
                # print("\tLength Maximum Reached: Shoot Prepared Message")
                await client.send_message(ctx.channel, lyrics_line_split)
                lyrics_line_split = l
                total_length = len(l)
            else:
                lyrics_line_split += l + "\n"

        # print("Lyrics to be Flushed: " + lyrics_line_split)
        return await client.send_message(ctx.channel, lyrics_line_split)
    else:
        return await client.send_message(ctx.channel, "No Lyrics")