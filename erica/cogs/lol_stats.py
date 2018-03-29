import regex
from discord import Embed
from discord.ext import commands

from erica.api.lol_api import get_summoner_info, get_league_positions, get_recent_matches, get_matches_stats


class LolStats():
    def __init__(self, bot):
        self.bot = bot

    def is_valid_username(self, summoner_name):
        return regex.match(r'^[0-9\p{L} _\.]+$', summoner_name)

    def kda(self, matches_info):
        k, d, a = 0, 0, 0

        for match_info in matches_info:
            k += match_info['kills']
            d += match_info['deaths']
            a += match_info['assists']

        return (a + k) / d

    def get_summoner_match_stats(self, matches_info, summoner_name):

        matches_summoner_info = []
        for match_info in matches_info:

            if not match_info:
                continue

            participant_identities = match_info['participantIdentities']
            summoner_participant_id_filter = [d['participantId'] for d in participant_identities if d['player']['summonerName'] == summoner_name]

            if summoner_participant_id_filter:
                participants = match_info['participants']
                matches_summoner_info.append(
                    [d['stats'] for d in participants if d['participantId'] == summoner_participant_id_filter[0]][0])

        return matches_summoner_info

    def build_description(self, summoner_info, elo_info, summoner_matches_info):
        description = f"Summoner Level -> {summoner_info['summonerLevel']}\n"

        if elo_info:
            description += f"Elo -> {elo_info['tier']} {elo_info['rank']}\n"
            description += f"League points -> {elo_info['leaguePoints']}\n"
            description += f"Wins -> {elo_info['wins']}\n"
            description += f"Losses -> {elo_info['losses']}\n"

        if summoner_matches_info:
            description += "Recent KDA -> {0:.2f}".format(self.kda(summoner_matches_info))

        return description

    @commands.command()
    async def lol(self, *summoner_name):

        # todo add cache layer

        summoner_name = " ".join(summoner_name)

        if not self.is_valid_username(summoner_name):
            return

        summoner_info = await get_summoner_info(self.bot.session, summoner_name)

        summoner_name = summoner_info['name']  # since $lol command is case insensitive and we want the real name

        if not summoner_info:
            return

        elo_info = await get_league_positions(self.bot.session, summoner_info['id'])
        elo_info = [elo for elo in elo_info if elo['queueType'] == 'RANKED_SOLO_5x5']

        solo_queue_info = elo_info[0] if elo_info else None

        recent_matches = await get_recent_matches(self.bot.session, summoner_info['accountId'])
        matches_info = await get_matches_stats(self.bot.session, recent_matches) if recent_matches else None
        summoner_matches_info = self.get_summoner_match_stats(matches_info, summoner_name) if matches_info else None

        await self.bot.say(embed=self.create_embed(summoner_name, description=self.build_description(summoner_info, solo_queue_info, summoner_matches_info)))

    # TODO every cog has its own embed
    def create_embed(self, title, description=None):
        em = Embed(title=title, description=description, color=0xf44242)
        em.set_author(name="League of Legends Stats")
        return em


def setup(bot):
    """
    This method is needed for this extension to be loaded properly by the bot.
    """
    bot.add_cog(LolStats(bot))
