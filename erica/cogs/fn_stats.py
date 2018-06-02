from discord.ext import commands

from erica.api.fn_api import get_player_info
from erica.cog import Cog

keys = ('Matches Played', 'Wins', 'Kills', 'K/d', 'Kills Per Min', 'Avg Survival Time', 'Win%')


class FortniteStats(Cog):
    def __init__(self, bot):
        Cog.__init__(self, name="Fornite Stats", color=0x406084)
        self.bot = bot

    @commands.command()
    async def fortnite(self, *player_nickname):
        """
        Retrieves the stats of a Fortnite player.

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


def setup(bot):
    """
    This method is needed for this extension to be loaded properly by the bot.
    """
    bot.add_cog(FortniteStats(bot))
