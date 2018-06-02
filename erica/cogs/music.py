import asyncio
import logging
from asyncio import Lock

from discord.ext import commands

from erica.api.yt_api import get_video_info, is_video_valid
from erica.cog import Cog
from erica.utils import get_param

logger = logging.getLogger(__name__)


class Song():
    """
    This class represents a song played by the MPlayer.
    """
    def __init__(self, title, id):
        self.url = "https://www.youtube.com/watch?v=" + id
        self.title = title


class MPlayer():
    """
    This class represents the music player used by the music cog to play music.
    """
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
        self.paused = False
        self.startup()

    def startup(self):
        """
        Starts the play loop without blocking.
        """
        asyncio.ensure_future(self.play())

    async def add_song_to_player(self):
        """
        Pops one song from the queue and puts it in the play queue.
        """
        song = self.queue.pop(0)
        await self.play_queue.put(song)

    async def next_with_last_check(self):
        """
        Checks if there is at least one song in the queue to process.
        If so it puts in the player otherwise the music player is reset(last song has been played and it is possible to
        left the voice channel).
        """
        if self.queue:
            await self.add_song_to_player()
        else:
            logging.info("Resetting music player")
            self.voice = None
            await self.cog.reset_music()

    async def add_song(self, song):
        """
        Adds a song to the queue.
        :param song: the song to be added.
        """
        self.queue.append(song)
        if len(self.queue) == 1 and self.curr_song is None:
            await self.add_song_to_player()

        await self.bot.send_message(self.channel, embed=self.cog.create_embed("Added song:", song.title))

    async def play(self):
        """
        This is the loop running the player.
        It processes song from the play queue.
        """
        while self.voice:
            self.curr_song = await self.play_queue.get()
            try:
                self.player = await self.voice.create_ytdl_player(self.curr_song.url, after=self.after_song)
                self.player.start()
            except:
                self.after_song()
            await self.bot.send_message(self.channel, embed=self.cog.create_embed("Now playing:", self.curr_song.title))

            # waiting until the next song need to be played(by checking the play_next flag)
            await self.play_next.wait()
            await self.next_with_last_check()

            # resetting the play_next flag
            self.play_next.clear()

    async def skip(self):
        """
        If the player is active, i.e. there is a song playing and the player is not paused, skips the current song.
        """
        if self.player and not self.paused:
            self.player.stop()
            await self.bot.send_message(self.channel, embed=self.cog.create_embed("Skipped song:", self.curr_song.title))

    async def playlist(self):
        """
        Generates the playlist given the songs in the queue and the current one.
        """
        description = ""

        playing_song = self.curr_song.title if self.curr_song and self.player and self.player.is_playing() else None
        if playing_song:
            description += f"Playing: {playing_song}\n"
        else:
            description += f"Player in pause\n"
        description += "Songs in queue:\n"
        for index, song in enumerate(self.queue, start=1):
            description += f"{index} - {song.title}\n"

        await self.bot.send_message(self.channel, embed=self.cog.create_embed('Playlist', description))

    async def pause(self):
        """
        Pauses the player.
        """
        if self.player:
            if self.player.is_playing():
                self.player.pause()
                self.paused = True
                await self.bot.send_message(self.channel, embed=self.cog.create_embed("Paused Player"))

    async def resume(self):
        """
        Resumes the player.
        """
        if self.player:
            if not self.player.is_playing():
                self.player.resume()
                self.paused = False
                await self.bot.send_message(self.channel, embed=self.cog.create_embed("Resumed Player"))

    async def remove(self, index):
        """
        Removes a song from the queue.
        :param index: the index of the songs in the queue.
        """
        if self.queue and 0 <= index < len(self.queue):
            song_removed = self.queue[index]
            del self.queue[index]
            await self.bot.send_message(self.channel, embed=self.cog.create_embed(title="Removed Song",
                                                                                  description=song_removed.title))

    def after_song(self):
        """
        This method is called by the external thread used for playing the song after the song is stopped/consumed.
        """
        self.bot.loop.call_soon_threadsafe(self.set_play_next)

    def set_play_next(self):
        """
        Sets the player to be ready to play the next song.
        """
        self.play_next.set()
        self.player = None
        self.curr_song = None


class Music(Cog):
    """
    This class represents the Music cog.
    It handles Erica's music commands for playing music.
    """
    def __init__(self, bot):
        Cog.__init__(self, "Music Player", 0xDEADBF)
        self.bot = bot
        self.mplayer = None
        self.voice = None
        self.voice_channel = None
        self.mplayer_lock = Lock()

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        """
        Plays a youtube song given the url.
        :param url: the url of the video
        """
        with (await self.mplayer_lock):

            video_id = get_param(url, "v")
            if not video_id:
                return

            video_info = await get_video_info(self.bot.session, video_id)
            if not video_info or not is_video_valid(video_info):
                return

            if not self.voice_channel:
                self.voice_channel = ctx.message.author.voice.voice_channel

                if not self.voice_channel:
                    return

                channel = ctx.message.channel

                try:
                    self.voice = await self.bot.join_voice_channel(self.voice_channel)
                except TimeoutError:
                    self.voice_channel = None
                    return

                logger.info(f"Joined channel {self.voice_channel}")
                self.mplayer = MPlayer(self, self.voice, channel)

            new_song = Song(video_info['items'][0]['snippet']['title'], video_id)
            await self.mplayer.add_song(new_song)

    @commands.command()
    async def playlist(self):
        """
        Shows the playlist.
        """
        if self.mplayer:
            with (await self.mplayer_lock):
                await self.mplayer.playlist()

    @commands.command()
    async def skip(self):
        """
        Skips the current song played.
        """
        if self.mplayer:
            with (await self.mplayer_lock):
                await self.mplayer.skip()

    @commands.command()
    async def pause(self):
        """
        Pauses the music player.
        """
        if self.mplayer:
            with (await self.mplayer_lock):
                await self.mplayer.pause()

    @commands.command()
    async def resume(self):
        """
        Resumes the music player.
        """
        if self.mplayer:
            with (await self.mplayer_lock):
                await self.mplayer.resume()

    @commands.command()
    async def remove(self, song_number):
        """
        Removes a song from the playlist.
        :param song_number: the number of the song in the playlist to be removed.
        """
        try:
            index = int(song_number)
        except ValueError:
            return

        if self.mplayer:
            with (await self.mplayer_lock):
                await self.mplayer.remove(index - 1)

    async def reset_music(self):
        """
        This method is called by the mplayer when all the songs have been consumed.
        It disconnects erica from the voice channel and deletes the music player.
        """
        await self.voice.disconnect()
        self.voice_channel = None
        self.mplayer = None


def setup(bot):
    """
    This method is needed for this extension to be loaded properly by the bot.
    """
    bot.add_cog(Music(bot))
