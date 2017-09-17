import requests
from common import *
from bs4 import BeautifulSoup

async def lyrics(lyric_auth, title : str, artist_name : str):
    search_url = lyric_auth["base_api_url"] + "/search?q=" + title
    data = {'q' : title}
    response = requests.get(search_url, data = data, headers = lyric_auth["headers"]  + lyric_auth["token"])
    json = response.json()
    song_info = None

    if str(json["meta"]["status"]).startswith(('4', '5')) :
        return await client.say("Error: " + json["meta"]["message"])

    for hit in json["response"]["hits"]:
        if artist_name in hit["result"]["primary_artist"]["name"]:
            song_info = hit
            break

    if song_info is not None:
        full_song_url = lyric_auth["base_song_url"] + song_info["result"]["path"]
        song_page = requests.get(full_song_url)
        html = BeautifulSoup(song_page.text, "html.parser")
        [h.extract() for h in html('script')]
        lyrics = html.find("div", class_="lyrics").get_text()
        lyrics_arr = lyrics.split("\n")

        arr_idx = 0
        total_length = 0
        lyrics_line_split = ""

        for l in lyrics_arr:
            print("Line: " + l)
            total_length += len(l)
            print("Total Length: " + str(total_length))
            if total_length >= 1700:
                print("\tLength Maximum Reached: Shoot Prepared Message")
                await client.say(lyrics_line_split)
                lyrics_line_split = l
                total_length = len(l)
            else:
                lyrics_line_split += l + "\n"

        print("Lyrics to be Flushed: " + lyrics_line_split)
        return await client.say(lyrics_line_split)
    else:
        return await client.say("No Lyrics")