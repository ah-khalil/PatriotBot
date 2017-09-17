from common import *

#connects the bot to the voice channel
async def connect(ctx):
    if client.is_voice_connected(ctx.message.server):
        return await client.say("I'm already connected to a voice channel")
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)