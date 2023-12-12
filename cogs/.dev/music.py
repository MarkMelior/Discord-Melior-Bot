import discord
import asyncio
import random
import youtube_dl
import string
import os
from discord.ext import commands
from googleapiclient.discovery import build
from discord.ext.commands import command
from dotenv import load_dotenv
import var
from pymongo import MongoClient



ytdl_format_options = {
    'audioquality': 5,
    'format': 'bestaudio',
    'outtmpl': '{}',
    'restrictfilenames': True,
    'flatplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    "extractaudio": True,
    "audioformat": "opus",
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# ЗАГРУЗКА youtube-dl НАСТРОЕК
ytdl_download_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.mp3',
    'reactrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_addreacs': '0.0.0.0',
    'output': r'youtube-dl',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
        }]
}

stim = {
    'default_search': 'auto',
    "ignoreerrors": True,
    'quiet': True,
    "no_warnings": True,
    "simulate": True,
    "nooverwrites": True,
    "keepvideo": False,
    "noplaylist": True,
    "skip_download": False,
    'source_address': '0.0.0.0'
}


ffmpeg_options = {
    'options': '-vn',
    #'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}


class Downloader(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get("url")
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')
        self.views = data.get('view_count')
        self.playlist = {}
        load_dotenv()

    @classmethod
    async def video_url(cls, url, ytdl, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        song_list = {'queue': []}
        if 'entries' in data:
            if len(data['entries']) > 1:
                playlist_titles = [title['title'] for title in data['entries']]
                song_list = {'queue': playlist_titles}
                song_list['queue'].pop(0)

            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), song_list

    async def get_info(self, url):
        yt = youtube_dl.YoutubeDL(stim)
        down = yt.extract_info(url, download=False)
        data1 = {'queue': []}
        if 'entries' in down:
            if len(down['entries']) > 1:
                playlist_titles = [title['title'] for title in down['entries']]
                data1 = {'title': down['title'], 'queue': playlist_titles}

            down = down['entries'][0]['title']

        return down, data1


class MusicPlayer( commands.Cog, name = 'Music' ):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient( var.MONGO_CLIENT )
        self.database = self.cluster.music.music
        self.music = self.database.find_one('music')
        self.player = {
            "audio_files": []
        }
        self.database_setup()

    def database_setup(self):
        URL = os.getenv("MONGO")
        if URL is None:
            return False

    @property
    def random_color(self):
        return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    async def yt_info(self, song):
        API_KEY = 'API_KEY'
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        song_data = youtube.search().list(part='snippet').execute()
        return song_data[0]

    @commands.Cog.listener('on_voice_state_update')
    async def music_voice(self, user, before, after):
        if after.channel is None and user.id == self.bot.user.id:
            try:
                self.player[user.guild.id]['queue'].clear()
            except KeyError:
                print(f"Не удалось получить ID гильдии {user.guild.id}")

    async def filename_generator(self):
        chars = list(string.ascii_letters+string.digits)
        name = ''
        for i in range(random.randint(9, 25)):
            name += random.choice(chars)

        if name not in self.player['audio_files']:
            return name

        return await self.filename_generator()

    async def playlist(self, data, msg):
        for i in data['queue']:
            print(i)
            self.player[msg.guild.id]['queue'].append(
                {'title': i, 'author': msg})

    async def queue(self, msg, song):
        title1 = await Downloader.get_info(self, url=song)
        title = title1[0]
        data = title1[1]
        if data['queue']:
            await self.playlist(data, msg)
            return await msg.send(f"Плейлист {data['title']} добавлен в очередь")
        self.player[msg.guild.id]['queue'].append(
            {'title': title, 'author': msg})
        return await msg.send(f"**{title} добавлен в очередь**".title())

    async def voice_check(self, msg):
        if msg.voice_client is not None:
            await asyncio.sleep(60) # функция, используемая для того, чтобы бот покинул голосовой канал, если музыка не воспроизводится более 2 минут
            if msg.voice_client is not None and msg.voice_client.is_playing() is False and msg.voice_client.is_paused() is False:
                await msg.voice_client.disconnect()

    async def clear_data(self, msg):
        name = self.player[msg.guild.id]['name']
        os.remove(name)
        self.player['audio_files'].remove(name)

    async def loop_song(self, msg):
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(self.player[msg.guild.id]['name']))
        loop = asyncio.get_event_loop()
        try:
            msg.voice_client.play(
                source, after=lambda a: loop.create_task(self.done(msg)))
            msg.voice_client.source.volume = self.player[msg.guild.id]['volume']
            if str(msg.guild.id) in self.music:
                msg.voice_client.source.volume = self.music['vol']/100
        except Exception as Error:
            print(Error)

    async def done(self, msg, msgId: int = None):
        if msgId:
            try:
                message = await msg.channel.fetch_message(msgId)
                await message.delete()
            except Exception as Error:
                print("Не удалось получить сообщение")

        if self.player[msg.guild.id]['reset'] is True:
            self.player[msg.guild.id]['reset'] = False
            return await self.loop_song(msg)

        if msg.guild.id in self.player and self.player[msg.guild.id]['repeat'] is True:
            return await self.loop_song(msg)

        await self.clear_data(msg)

        if self.player[msg.guild.id]['queue']:
            queue_data = self.player[msg.guild.id]['queue'].pop(0)
            return await self.start_song(msg=queue_data['author'], song=queue_data['title'])

        else:
            await self.voice_check(msg)

    async def start_song(self, msg, song):
        new_opts = ytdl_format_options.copy()
        audio_name = await self.filename_generator()

        self.player['audio_files'].append(audio_name)
        new_opts['outtmpl'] = new_opts['outtmpl'].format(audio_name)

        ytdl = youtube_dl.YoutubeDL(new_opts)
        download1 = await Downloader.video_url(song, ytdl=ytdl, loop=self.bot.loop)
        download = download1[0]
        data = download1[1]
        self.player[msg.guild.id]['name'] = audio_name
        emb = discord.Embed(colour=self.random_color, title='Сейчас играет',
                            description=download.title, url=download.url)
        emb.set_thumbnail(url=download.thumbnail)
        emb.set_footer(
            text=f'Включил музыку: {msg.author.display_name}', icon_url=msg.author.avatar_url)
        loop = asyncio.get_event_loop()

        if data['queue']:
            await self.playlist(data, msg)

        msgId = await msg.send(embed=emb)
        self.player[msg.guild.id]['player'] = download
        self.player[msg.guild.id]['author'] = msg
        msg.voice_client.play(
            download, after=lambda a: loop.create_task(self.done(msg, msgId.id)))

        if str(msg.guild.id) in self.music: #NOTE adds user's default volume if in database
            msg.voice_client.source.volume=self.music[str(msg.guild.id)]['vol']/100
        msg.voice_client.source.volume = self.player[msg.guild.id]['volume']
        return msg.voice_client

    @command( aliases = var.aMusicPlay, brief = var.bMusicPlay, usage = var.uMusicPlay )
    async def __play(self, msg, *, song):
        if msg.guild.id in self.player:
            if msg.voice_client.is_playing() is True:
                return await self.queue(msg, song)

            if self.player[msg.guild.id]['queue']:
                return await self.queue(msg, song)

            if msg.voice_client.is_playing() is False and not self.player[msg.guild.id]['queue']:
                return await self.start_song(msg, song)

        else:
            self.player[msg.guild.id] = {
                'player': None,
                'queue': [],
                'author': msg,
                'name': None,
                "reset": False,
                'repeat': False,
                'volume': 0.5
            }
            return await self.start_song(msg, song)

    @__play.before_invoke
    async def before_play(self, msg):

        if msg.author.voice is None:
            return await msg.send('**Пожалуйста, присоединись к тому же голосовому каналу, что и я, для воспроизведения музыки**'.title())

        if msg.voice_client is None:
            return await msg.author.voice.channel.connect()

        if msg.voice_client.channel != msg.author.voice.channel:

            if msg.voice_client.is_playing() is False and not self.player[msg.guild.id]['queue']:
                return await msg.voice_client.move_to(msg.author.voice.channel)

            if self.player[msg.guild.id]['queue']:
                return await msg.send("Пожалуйста, присоединись к тому же голосовому каналу, что и я, чтобы добавить песню в очередь")

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicRepeat, brief = var.bMusicRepeat, usage = var.uMusicRepeat )
    async def __repeat(self, msg):
        if msg.guild.id in self.player:
            if msg.voice_client.is_playing() is True:
                if self.player[msg.guild.id]['repeat'] is True:
                    self.player[msg.guild.id]['repeat'] = False
                    return await msg.message.add_reaction(emoji='✅')

                self.player[msg.guild.id]['repeat'] = True
                return await msg.message.add_reaction(emoji='✅')

            return await msg.send("В данный момент звук не воспроизводится")
        return await msg.send("Я не в голосовом канале и музыка сейчас не играет")

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicReset, brief = var.bMusicReset, usage = var.uMusicReset )
    async def __reset(self, msg):
        if msg.voice_client is None:
            return await msg.send(f"**{msg.author.display_name}, в настоящее время нет звука, увы**")

        if msg.author.voice is None or msg.author.voice.channel != msg.voice_client.channel:
            return await msg.send(f"**{msg.author.display_name}, ты должен`на` находиться в том же голосовом канале, что и я.**")

        if self.player[msg.guild.id]['queue'] and msg.voice_client.is_playing() is False:
            return await msg.send("**В данный момент не воспроизводится музыка в очереди**".title(), delete_after=25)

        self.player[msg.guild.id]['reset'] = True
        msg.voice_client.stop()

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicSkip, brief = var.bMusicSkip, usage = var.uMusicSkip )
    async def __skip(self, msg):
        if msg.voice_client is None:
            return await msg.send("**В настоящее время музыка не играет**".title(), delete_after=60)

        if msg.author.voice is None or msg.author.voice.channel != msg.voice_client.channel:
            return await msg.send("Пожалуйста, присоединись к тому же голосовому каналу, что и я")

        if not self.player[msg.guild.id]['queue'] and msg.voice_client.is_playing() is False:
            return await msg.send("**Нет музыки в очереди, чтобы пропустить**".title(), delete_after=60)

        self.player[msg.guild.id]['repeat'] = False
        msg.voice_client.stop()
        return await msg.message.add_reaction(emoji='✅')

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicStop, brief = var.bMusicStop, usage = var.uMusicStop )
    async def __stop(self, msg):
        if msg.voice_client is None:
            return await msg.send("Я нахожусь не в голосовом канале, чтобы остановить музыку")

        if msg.author.voice is None:
            return await msg.send("Ты должен`на` находиться в том же голосовом канале, что и я")

        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_playing() is True or self.player[msg.guild.id]['queue']:
                self.player[msg.guild.id]['queue'].clear()
                self.player[msg.guild.id]['repeat'] = False
                msg.voice_client.stop()
                return await msg.message.add_reaction(emoji='✅')

            return await msg.send(f"**{msg.author.display_name}, в настоящее время не воспроизводится музыка в очереди**")

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicLeave, brief = var.bMusicLeave, usage = var.uMusicLeave )
    async def __leave(self, msg):
        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_playing() is True or self.player[msg.guild.id]['queue']:
                self.player[msg.guild.id]['queue'].clear()
                msg.voice_client.stop()
                return await msg.voice_client.disconnect(), await msg.message.add_reaction(emoji='✅')

            return await msg.voice_client.disconnect(), await msg.message.add_reaction(emoji='✅')

        if msg.author.voice is None:
            return await msg.send("Ты должен быть в том же голосовом канале, что и я, чтобы отключить меня")

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicPause, brief = var.bMusicPause, usage = var.uMusicPause )
    async def __pause(self, msg):
        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_paused() is True:
                return await msg.send("Музыка и так уже остановлена как бы ._ .")

            if msg.voice_client.is_paused() is False:
                msg.voice_client.pause()
                await msg.message.add_reaction(emoji='✅')

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicResume, brief = var.bMusicResume, usage = var.uMusicResume )
    async def __resume(self, msg):
        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_paused() is False:
                return await msg.send("Музыка уже играет как бы ._ .")

            if msg.voice_client.is_paused() is True:
                msg.voice_client.resume()
                return await msg.message.add_reaction(emoji='✅')

    @command( aliases = var.aMusicQueue, brief = var.bMusicQueue, usage = var.uMusicQueue )
    async def __queue(self, msg):
        if msg.voice_client is not None:
            if msg.guild.id in self.player:
                if self.player[msg.guild.id]['queue']:
                    emb = discord.Embed(
                        colour=self.random_color, title='queue')
                    emb.set_footer(
                        text=f'Команду вызвал: {msg.author.name}', icon_url=msg.author.avatar_url)
                    for i in self.player[msg.guild.id]['queue']:
                        emb.add_field(
                            name=f"**{i['author'].author.name}**", value=i['title'], inline=False)
                    return await msg.send(embed=emb, delete_after=120)

        return await msg.send("Нет песен в очереди")

    @command( aliases = var.aMusicInfo, brief = var.bMusicInfo, usage = var.uMusicInfo )
    async def __song_info(self, msg):
        if msg.voice_client is not None and msg.voice_client.is_playing() is True:
            emb = discord.Embed(colour=self.random_color, title='Currently Playing',
                                description=self.player[msg.guild.id]['player'].title)
            emb.set_footer(
                text=f"{self.player[msg.guild.id]['author'].author.name}", icon_url=msg.author.avatar_url)
            emb.set_thumbnail(
                url=self.player[msg.guild.id]['player'].thumbnail)
            return await msg.send(embed=emb, delete_after=120)

        return await msg.send(f"**В настоящее время песня не воспроизводится**".title(), delete_after=30)

    @command( aliases = var.aMusicJoin, brief = var.bMusicJoin, usage = var.uMusicJoin )
    async def __join(self, msg, *, channel: discord.VoiceChannel = None):
        if msg.voice_client is not None:
            return await msg.send(f"Я уже в голосовом канале \n Ты хотел использовать {msg.prefix}moveTo")

        if msg.voice_client is None:
            if channel is None:
                return await msg.author.voice.channel.connect(), await msg.message.add_reaction(emoji='✅')

            return await channel.connect(), await msg.message.add_reaction(emoji='✅')

        else:
            if msg.voice_client.is_playing() is False and not self.player[msg.guild.id]['queue']:
                return await msg.author.voice.channel.connect(), await msg.message.add_reaction(emoji='✅')

    @__join.before_invoke
    async def __before_join(self, msg):
        if msg.author.voice is None:
            return await msg.send("Ты не в голосовом канале")

    @__join.error
    async def join_error(self, msg, error):
        if isinstance(error, commands.BadArgument):
            return msg.send(error)

        if error.args[0] == 'Command raised an exception: Exception: playing':
            return await msg.send("**Пожалуйста, присоединись к тому же голосовому каналу, что и я, чтобы добавить песню в очередь**".title())

    @commands.has_permissions(manage_channels=True)
    @command( aliases = var.aMusicVolume, brief = var.bMusicVolume, usage = var.uMusicVolume )
    async def __volume(self, msg, vol: int):
        if vol > 200:
            vol = 200
        vol = vol/100
        if msg.author.voice is not None:
            if msg.voice_client is not None:
                if msg.voice_client.channel == msg.author.voice.channel and msg.voice_client.is_playing() is True:
                    msg.voice_client.source.volume = vol
                    self.player[msg.guild.id]['volume'] = vol
                    if (msg.guild.id) in self.music:
                        self.music[str(msg.guild.id)]['vol']=vol
                    return await msg.message.add_reaction(emoji='✅')

        return await msg.send("**Пожалуйста, присоединись к тому же голосовому каналу, что и я, чтобы использовать команду**".title(), delete_after=30)

    @commands.command( aliases = var.aMusicDownload, brief = var.bMusicDownload, usage = var.uMusicDownload )
    async def __download(self, ctx, *, song):
        try:
            with youtube_dl.YoutubeDL(ytdl_download_format_options) as ydl:
                if "https://www.youtube.com/" in song:
                    download = ydl.extract_info(song, True)
                else:
                    infosearched = ydl.extract_info(
                        "ytsearch:"+song, False)
                    download = ydl.extract_info(
                        infosearched['entries'][0]['webpage_url'], True)
                filename = ydl.prepare_filename(download)
                embed = discord.Embed(
                    title="Ваша загрузка готова", description="Пожалуйста, подожди немножко, пока я скачаю)")
                await ctx.send(embed=embed, delete_after=30)
                await ctx.send(file=discord.File(filename))
                os.remove(filename)
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            embed = discord.Embed(title="Мне не удалось загрузить песню :<", description=("Song:"+song))
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(MusicPlayer(bot))