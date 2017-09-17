import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup

Client = discord.Client()
description = "A bot that does random things"
client = commands.Bot(description = description, command_prefix = "t.")

token = "M_loAkgGcYsPKisCW2h1FEOKFq7sOLGNwP16YR-koHq7yYWs6aulN5CvPRBrxLUQ"
base_api_url = "http://api.genius.com"
base_song_url = "http://genius.com"
headers = {'Authorization' : 'Bearer ' + token}

@client.command(pass_context=True)
async def close(ctx):
    print(ctx.message.author)
    if "khalilashnikov" in ctx.message.author.name:
        await client.say("Bye y'all")
        return await client.logout()

@client.command(pass_context=True)
async def status(ctx):
    return await client.change_status(ctx.message.content)

#connects the bot to the voice channel
@client.command(pass_context=True)
async def connect(ctx):
    if client.is_voice_connected(ctx.message.server):
        return await client.say("I'm already connected to a voice channel")
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)

@client.command(pass_context=True)
async def disconnect(ctx):
    if not client.is_voice_connected(ctx.message.server):
        return await client.say("I'm not connected to any voice channel")
    for vc in client.voice_clients:
        if vc.server == ctx.message.server:
            return await vc.disconnect()

@client.command()
async def lyrics(title : str, artist_name : str):
    search_url = base_api_url + "/search?q=" + title
    data = {'q' : title}
    response = requests.get(search_url, data = data, headers = headers)
    json = response.json()
    song_info = None

    if str(json["meta"]["status"]).startswith(('4', '5')) :
        return await client.say("Error: " + json["meta"]["message"])

    for hit in json["response"]["hits"]:
        if artist_name in hit["result"]["primary_artist"]["name"]:
            song_info = hit
            break

    if song_info is not None:
        full_song_url = base_song_url + song_info["result"]["path"]
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

@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print('---------------------------------')


client.run("MzE3NTk2MzQ2Mjc2MzgwNjc0.DDT6hw.lT8BKjPh2h86tosVH02o76S_TFI")
