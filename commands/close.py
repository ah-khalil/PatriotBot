from common import *

async def close(ctx):
    if "khalilashnikov" in ctx.author.name:
        await client.say("Bye y'all")
        return await client.logout()