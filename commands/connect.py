from common import *

#connects the bot to the voice channel
async def connect(ctx):
    if client.is_voice_connected(ctx.server):
        return await client.send_message(ctx.channel, "I'm already connected to a voice channel")
    if ctx.author.voice_channel == None:
        return await client.send_message(ctx.channel, "@{}, you should be connected to a voice channel".format(ctx.author))
    return await client.join_voice_channel(ctx.author.voice_channel)