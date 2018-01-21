import discord
from discord.ext import commands
import logging

DESCRIPTION = '''
list all help commands here
'''
EXTENSIONS = ["basic", "music"]


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not discord.opus.is_loaded():
    # this is required for playing sounds
    discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')

bot = commands.Bot(command_prefix="$", description=DESCRIPTION)

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    print("\n")

@bot.event
async def on_command_error(error, ctx):
    logging.info(f"{error} Occurred in {ctx.command} command")


if __name__ == "__main__":
    for extension in EXTENSIONS:
        try:
            bot.load_extension("cogs." + extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")
            print(f"{e}")

        bot.run("token")
