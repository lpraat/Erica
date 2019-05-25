import asyncio
import discord
import aiohttp
import logging

from discord.ext.commands import Bot
from erica.cogs import Basic, Music, LolStats, FortniteStats

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Erica(Bot):
    """
    The Erica bot.
    """

    COGS = [Basic, Music, LolStats, FortniteStats]

    DESCRIPTION = """
    Code Red Dustin, Code Red.
    """

    def __init__(self, command_prefix, **options):
        Bot.__init__(self, command_prefix, **options)
        self.session = None

        asyncio.wait(asyncio.ensure_future(self.load_cogs()))
        asyncio.wait(asyncio.ensure_future(self.load_session()))

    async def load_session(self):
        self.session = await aiohttp.ClientSession().__aenter__()

    async def on_command_error(self, ctx, exception):
        logging.info(f"Error in {ctx.command} command: {exception}")

    async def on_ready(self):
        logging.info("Logged in as " + self.user.name)

    async def load_cogs(self):
        for cog in Erica.COGS:
            try:
                self.add_cog(cog(self))
                logger.info(f"Added cog {cog.__name__}")
            except discord.ClientException as e:
                logger.info(f"Failed to load cog {cog.__name__}")
                logger.info(f"{e}")