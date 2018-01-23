import discord
import logging
from os import getenv
import asyncio
from erica.erica_bot import Erica

DESCRIPTION = '''
Code Red Dustin, Code Red.
'''
EXTENSIONS = ["basic", "music"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not discord.opus.is_loaded():
    # this is required for playing sounds
    # TODO change the path with the docker container one
    discord.opus.load_opus('/usr/local/Cellar/opus/1.2.1/lib/')

bot = Erica(command_prefix="$", description=DESCRIPTION)


@bot.event
async def on_ready():
    logging.info("Logged in as " + bot.user.name)

@bot.event
async def on_command_error(error, ctx):
    logging.info(f"{error} Occurred in {ctx.command} command")


async def load_extension():
    """
    Loads all the cogs.
    """
    for extension in EXTENSIONS:
        try:
            bot.load_extension("cogs." + extension)
            logger.info(f"Added extension {extension}")
        except Exception as e:
            logger.info(f"Failed to load extension {extension}")
            logger.info(f"{e}")


if __name__ == "__main__":
    asyncio.wait(asyncio.ensure_future(load_extension()))
    bot.run(getenv('TOKEN'))
