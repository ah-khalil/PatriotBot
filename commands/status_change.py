from common import *

async def status_change(ctx):
    game_name = ctx.content.split(" ")[1]
    print(game_name)
    await client.change_presence(game = discord.Game(name=game_name))