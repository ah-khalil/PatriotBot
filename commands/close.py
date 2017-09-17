from common import *

async def close(ctx):
    print(ctx.message.author)
    if "khalilashnikov" in ctx.message.author.name:
        await client.say("Bye y'all")
        return await client.logout()