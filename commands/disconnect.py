from common import *

async def disconnect(ctx):
    if not client.is_voice_connected(ctx.message.server):
        return await client.say("I'm not connected to any voice channel")
    for vc in client.voice_clients:
        if vc.server == ctx.message.server:
            return await vc.disconnect()