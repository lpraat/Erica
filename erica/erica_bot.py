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
    

