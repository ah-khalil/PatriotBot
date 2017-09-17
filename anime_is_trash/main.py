import discord
import pkgutil
import sys
import os

_prefix = 't'
lib_path = os.path.abspath(os.path.join('commands'))
sys.path.append(lib_path)

import commands

pkgpath = os.path.dirname(commands.__file__)
for name in pkgutil.iter_modules(pkgpath):
    print("Module: {}".format(name))
client = discord.Client();

async def on_ready():
    print("Logged in as {} ").format(client.user.name, client.user.id)
    print("=========================================================")

@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if message.content.startswith(_prefix):
            pass


