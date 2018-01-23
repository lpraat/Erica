import aiohttp
from discord.ext.commands import Bot


class Erica(Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        self.session = aiohttp.ClientSession()
