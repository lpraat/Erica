from discord import Embed
from discord.ext import commands
import logging
import asyncio
from asyncio import Lock

from erica.api.yt_api import get_video_info, is_video_valid
from erica.utils import get_param

logger = logging.getLogger(__name__)


class Song():
    def __init__(self, title, id):
        self.url = "https://www.youtube.com/watch?v=" + id
        self.title = title


class MPlayer():
    def __init__(self, cog, voice, channel):
        self.cog = cog
        self.bot = cog.bot
        self.voice = voice
        self.channel = channel
        self.queue = []
        self.play_queue = asyncio.Queue(loop=self.bot.loop)
        self.play_next = asyncio.Event()
        self.player = None
        self.curr_song = None
        self.startup()

    def startup(self):
        asyncio.ensure_future(self.play())

    async def add_song_to_player(self):
        song = self.queue.pop(0)
        await self.play_queue.put(song)

    async def next_with_last_check(self):
        if self.queue:
            await self.add_song_to_player()
        else:
            self.voice = None
            await self.cog.reset_music()

    async def add_song(self, song):
        self.queue.append(song)
        if len(self.queue) == 1 and self.curr_song == None:
            await self.add_song_to_player()

        await self.bot.send_message(self.channel, embed=self.get_embed("Added song:", song.title))

    async def play(self):
        while self.voice:
            self.curr_song = await self.play_queue.get()
            self.player = await self.voice.create_ytdl_player(self.curr_song.url, after=self.after_song)
            self.player.start()
            await self.bot.send_message(self.channel, embed=self.get_embed("Now playing:", self.curr_song.title))
            await self.play_next.wait()
            await self.next_with_last_check()
            self.play_next.clear()

    async def skip(self):
        if self.player:
            self.player.stop()
            await self.bot.send_message(self.channel, embed=self.get_embed("Skipped song:", self.curr_song.title))

    def get_embed(self, title, description=None):
        em = Embed(title=title, description=description, color=0xDEADBF)
        em.set_author(name="Music Player")
        return em

    async def playlist(self):
        print(self.queue)
        description = ""

        playing_song = self.curr_song.title if self.curr_song and self.player and self.player.is_playing() else None
        if playing_song:
            description += f"Playing: {playing_song}\n"
        else:
            description += f"Player in pause\n"
        description += "Songs in queue:\n"
        for index, song in enumerate(self.queue, start=1):
            description += f"{index} - {song.title}\n"

        await self.bot.send_message(self.channel, embed=self.get_embed('Playlist', description))

    async def pause(self):
        if self.player:
            if self.player.is_playing():
                self.player.pause()
                await self.bot.send_message(self.channel, embed=self.get_embed("Paused Player"))

    async def resume(self):
        if self.player:
            if not self.player.is_playing():
                self.player.resume()
                await self.bot.send_message(self.channel, embed=self.get_embed("Resumed Player"))

    async def remove(self, index):
        if self.queue and 0 < index < len(self.queue):
            print("sono qua")
            song_removed = self.queue[index]
            del self.queue[index]
            await self.bot.send_message(self.channel, embed=self.get_embed(title="Removed Song",
                                                                           description=song_removed.title))

    def after_song(self):
        self.bot.loop.call_soon_threadsafe(self.set_play_next)

    def set_play_next(self):
        self.play_next.set()
        self.player = None
        self.curr_song = None


class Music():
    def __init__(self, bot):
        self.bot = bot
        self.m_player = None
        self.voice_channel = None
        self.mplayer_lock = Lock()

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        with (await self.mplayer_lock):

            video_id = get_param(url, "v")
            print(video_id)
            if not video_id:
                return

            video_info = await get_video_info(self.bot.session, video_id)
            if not is_video_valid(video_info):
                return

            if not self.voice_channel:
                self.voice_channel = ctx.message.author.voice.voice_channel

                if not self.voice_channel:
                    return

                channel = ctx.message.channel
                self.voice = await self.bot.join_voice_channel(self.voice_channel)
                logger.info(f"Joined channel {self.voice_channel}")

                self.m_player = MPlayer(self, self.voice, channel)

            new_song = Song(video_info['items'][0]['snippet']['title'], video_id)
            await self.m_player.add_song(new_song)

    @commands.command()
    async def playlist(self):
        if self.m_player:
            with (await self.mplayer_lock):
                await self.m_player.playlist()

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        if self.m_player:
            with (await self.mplayer_lock):
                await self.m_player.skip()

    @commands.command()
    async def pause(self):
        if self.m_player:
            with (await self.mplayer_lock):
                await self.m_player.pause()

    @commands.command()
    async def resume(self):
        if self.m_player:
            with (await self.mplayer_lock):
                await self.m_player.resume()

    @commands.command()
    async def remove(self, song_number):

        try:
            index = int(song_number)
        except ValueError:
            return

        if self.m_player:
            with (await self.mplayer_lock):
                await self.m_player.remove(index - 1)

    async def reset_music(self):
        await self.voice.disconnect()
        self.voice_channel = None
        self.m_player = None


def setup(bot):
    bot.add_cog(Music(bot))
