from discord import Embed
from discord.ext import commands

from erica.api.fn_api import get_player_info

keys = ('Matches Played', 'Wins', 'Kills', 'K/d', 'Kills Per Min', 'Avg Survival Time')


class Stats():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fortnite(self, *player_nickname):
        """
        Retrieves the player fortnite stats given its nickname.

        :param player_nickname: the player's nickname.
        """
        player_nickname = " ".join(player_nickname)
        player_stats = {}

        result = await get_player_info(self.bot.session, player_nickname)

        if 'error' not in result:
            life_time_stats = result['lifeTimeStats']

            for stat in life_time_stats:
                if stat['key'] in keys:
                    player_stats.update({stat['key']: stat['value']})

            description = ""

            for (key, value) in player_stats.items():
                description += key + " -> " + value + "\n"

            await self.bot.say(embed=self.create_embed(player_nickname, description=description))

    # TODO every cog has its own embed
    def create_embed(self, title, description=None):
        em = Embed(title=title, description=description, color=0x406084)
        em.set_author(name="Fornite Stats")
        return em


def setup(bot):
    """
    This method is needed for this extension to be loaded properly by the bot.
    """
    bot.add_cog(Stats(bot))
