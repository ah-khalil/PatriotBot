from customerrors import *
from common import *
import pkgutil
import json

_prefix = 't?'
mod_list = []
[mod_list.append(name) for _, name, _ in pkgutil.iter_modules(['commands'])]

with open('config.json') as config:
    auth = json.load(config)

async def on_ready():
    print("Logged in as {} ").format(client.user.name, client.user.id)
    print("=========================================================")

@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if message.content.startswith(_prefix):
            #code to iterate through the module list and add the message author's
            #timer as a sub-array to that module
            try:
                msg_split = message.content.split(" ")
                com_split = msg_split[0].split("?")

                if com_split[1] not in mod_list:
                    raise CommandNotFoundException()
            except CommandNotFoundException:
                await client.say("The following command was not found: {}".format(com_split[1]))



client.run(auth["discord_client_auth"]["token"])
