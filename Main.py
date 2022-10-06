import discord 
from discord.ext import commands 
import datetime 
import typing
import youtube_dl

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='A!', description="Hola Soy un Bot ", intents=intents)

TOKEN = '<your discord token>'

#Comandos
@bot.command()
async def ping(ctx, name='ping', help='juega al ping pong'):
     await ctx.send('pong')

@bot.command()
async def bottles(ctx, amount: typing.Optional[int] = 99, *, liquid='beer', name='bottles', help='Cuantas botellas hay en la barra?'):
    await ctx.send(f"{amount} botellas de {amount} en la barra")

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='ninguna razon', name='slap', help='Da una bofetada a alguien del chat'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send(f'{slapped} acaba de recibir una bofetada por {reason}')

@bot.command()
async def best(ctx, members: commands.Greedy[discord.Member], name='best', help='Pronuncias a alguien o a ti mejor en el servidor'):
    user = ", ".join(x.name for x in members)
    await ctx.send(f"**{user}** es el mejor en el server")


#Youtube Player 
@bot.command(name='unirse', help='le dices al Bot que se una a un canal de voz')
async def unirse(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} no esta conectado a un canal de voz".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect(self_deaf=True)

@bot.command(name='irse', help='Haces que el Bot salga del canal de voz')
async def irse(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("El Bot no esta en un canal de voz")

@bot.command(name='play', help='Reproduce una cancion')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Reproduciendo:** {}'.format(filename))
    except:
        await ctx.send("El Bot no esta conectada a un canal de voz.")


@bot.command(name='pause', help='Pausa la cancion')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("Estoy comodo en un canal de voz y no me quiero mover")
    
@bot.command(name='resume', help='Continua la cancion')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("El Bot no esta reproduciendo ninguna cancion usa play para reproducir")

@bot.command(name='stop', help='Detiene la cancion')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("El Bot no esta en ninguna cancion en este momento")

#Dependencias
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download='stream'))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


#Ajustes Finales del bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="cosas en internet"))
    print('Aurora esta en linea')

bot.run(TOKEN)
