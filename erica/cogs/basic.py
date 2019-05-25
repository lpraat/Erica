import logging
import random

from discord.ext import commands
from erica.cog import Cog

logger = logging.getLogger(__name__)


class Basic(Cog):
    """
    Basic cog.
    It handles Erica's basic commands.
    """

    ASK_ANSWERS = {
        '1': "Yes! Definitely.",
        '2': "I'm absolutely sure!",
        '3': "I think so, but I'm not completely sure. You better ask my brother!",
        '4': "I don't think so. You better ask Lucas!",
        '5': "Shut your mouth, nerd!",
        '6': "Yeeee.. NO!",
        '7': "Nope!",
        '8': "Don't know. Don't care."
    }

    def __init__(self, bot):
        Cog.__init__(self, "basic")
        self.bot = bot

    @commands.command()
    async def repeat(self, ctx, times, *message):
        """
        Repeats a message by speaking out loudly.
        :param times: the number of times the message needs to be repeated.
        :param the message: the message to be repeated.
        """
        try:
            times = int(times)
        except ValueError:
            logger.info("Time in repeat command must be integer")

        times = min(times, 20)  # repeat at maximum 20 times

        for i in range(times):
            await ctx.send(" ".join(message), tts=True)

    @commands.command()
    async def ask(self, ctx, *question):
        """Try Erica Magic 8 Ball.
        :param question: the question asked.
        """

        if "?" not in " ".join(question):
            await ctx.send("That's not a question, fella!")
        else:
            answer = self.ASK_ANSWERS.get(str(random.randint(1, len(self.ASK_ANSWERS))))
            await ctx.send(answer)


def setup(bot):
    """
    This is needed for this extension to be loaded properly by the bot.
    """
    bot.add_cog(Basic(bot))
