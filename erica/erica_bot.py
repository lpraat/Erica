import asyncio

import aiohttp
from discord.ext.commands import Bot


class Erica(Bot):
    """
    The Erica bot.
    """

    def __init__(self, command_prefix, **options):
        Bot.__init__(self, command_prefix, **options)
        self.session = None

        asyncio.wait(asyncio.ensure_future(self.load_session()))

    async def load_session(self):
        self.session = await aiohttp.ClientSession().__aenter__()
