import aiohttp
import asyncio
from discord.ext.commands import Bot


class Erica(Bot):
    """
    This class represent the Erica bot.
    It extends the Bot class provided by the discord.py.
    """

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
<<<<<<< HEAD
        asyncio.wait(asyncio.ensure_future(self.load_session()))

    async def load_session(self):
        self.session = await aiohttp.ClientSession().__aenter__()
=======
    
>>>>>>> 286a9611898bfd0c762228ea1120810b170a2f71

