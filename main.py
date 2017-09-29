from customerrors.CommandNotFoundError import CommandNotFoundError

from commands.close import close
from commands.connect import connect
from commands.disconnect import disconnect
from commands.lyrics import lyrics
from commands.status_change import status_change

from common import *
import time
import pkgutil

_prefix = 't?'
mod_list = {}

for _, name, _ in pkgutil.iter_modules(['commands']):
    mod_list[name] = {}

async def on_ready():
    print("Logged in as {} ").format(client.user.name, client.user.id)
    print("=========================================================")

@client.event
async def on_message(ctx):
    if ctx.author.id != client.user.id:
        if ctx.content.startswith(_prefix):
            #code to iterate through the module list and add the message author's
            #timer as a sub-list to that module
            msg_split = []
            com_split = []

            try:
                now = time.time()
                msg_split = ctx.content.split(" ")
                com_split = msg_split[0].split("?")

                if com_split[1] not in mod_list:
                    raise CommandNotFoundError()

                if ctx.author.id not in mod_list[com_split[1]]:
                    mod_list[com_split[1]] = {ctx.author.id : ""}

                if mod_list[com_split[1]][ctx.author.id] == "" or mod_list[com_split[1]][ctx.author.id] + 10.0 < now:
                    mod_list[com_split[1]][ctx.author.id] = now
                    del msg_split[0]
                    await globals()[com_split[1]](ctx)
                else:
                    await client.send_message(ctx.channel, "@{}, you need to wait for at least ten seconds before using that command again".format(ctx.author.name))

            except CommandNotFoundError:
                await client.send_message(ctx.channel, "The following command was not found: {}".format(com_split[1]))

client.run(auth["discord_client_auth"]["token"])
