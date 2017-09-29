import discord
import json

client = discord.Client();
description = "A bot that does random things"
with open('config.json') as config:
    auth = json.load(config)
