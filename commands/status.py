from common import *

async def status(ctx):
    return await client.change_status(ctx.message.content)