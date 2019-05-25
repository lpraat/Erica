import asyncio
import logging
import discord

from erica.erica_bot import Erica
from erica.cogs import Basic
from os import getenv

DESCRIPTION = """
Code Red Dustin, Code Red.
"""

if not discord.opus.is_loaded():
    # this is required for playing sounds
    discord.opus.load_opus(getenv('OPUS_PATH'))

bot = Erica(command_prefix="$", description=DESCRIPTION)

if __name__ == "__main__":
    bot.run(getenv('TOKEN'))
