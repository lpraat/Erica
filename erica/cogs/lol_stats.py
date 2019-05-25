import regex

from discord.ext import commands
from erica.api.lol_api import get_summoner_info, get_league_info, get_recent_matches, get_matches_stats
from erica.cog import Cog


class LolStats(Cog):
    def __init__(self, bot):
        Cog.__init__(self, "League of Legends Stats", 0xf44242)
        self.bot = bot

    def is_valid_username(self, summoner_name):
        """
        Checks if the username is a valid one. This method uses the regex provided by the Riot API.
        :param summoner_name: the summoner name.
        :return: true if username is valid, false otherwise.
        """
        return regex.match(r'^[0-9\p{L} _\.]+$', summoner_name)

    def kda(self, matches_stats):
        """
        Calculates the kda given a set of matches.
        :param matches_stats: the matches stats.
        :return: the kda value.
        """
        k, d, a = 0, 0, 0

        for match_info in matches_stats:
            k += match_info['kills']
            d += match_info['deaths']
            a += match_info['assists']

        return (a + k) / d

    def get_summoner_match_stats(self, matches_stats, summoner_name):
        """
        Finds a summoner personal stats in a set of matches.
        :param matches_stats: the matches stats.
        :param summoner_name: the summoner name.
        :return: a list of dict containing the summoner stats.
        """
        matches_summoner_stats = []
        for match_info in matches_stats:

            if not match_info:
                continue

            participant_identities = match_info['participantIdentities']
            summoner_participant_id_filter = [d['participantId'] for d in participant_identities if
                                              d['player']['summonerName'] == summoner_name]

            if summoner_participant_id_filter:
                participants = match_info['participants']
                matches_summoner_stats.append(
                    [d['stats'] for d in participants if d['participantId'] == summoner_participant_id_filter[0]][0])

        return matches_summoner_stats

    def build_description(self, summoner_info, elo_info, summoner_matches_stats):
        """
        Prepares the description of the embed that will be output to the discord chat. It build it using the summoner,
        the elo info and the stats of recent matches.
        :param summoner_info: the summmoner info.
        :param elo_info: the elo info.
        :param summoner_matches_stats: the stats of recent matches of the summoner.
        :return: a string representing the embed description.
        """
        description = f"Summoner Level -> {summoner_info['summonerLevel']}\n"

        if elo_info:
            description += f"Elo -> {elo_info['tier']} {elo_info['rank']}\n"
            description += f"League points -> {elo_info['leaguePoints']}\n"
            description += f"Wins -> {elo_info['wins']}\n"
            description += f"Losses -> {elo_info['losses']}\n"

        if summoner_matches_stats:
            description += "Recent KDA -> {0:.2f}".format(self.kda(summoner_matches_stats))

        return description

    @commands.command()
    async def lol(self, ctx, *summoner_name):
        """
        Retrieves the stats of a League of Legends player.
        :param summoner_name: the player's summoner name.
        """
        summoner_name = " ".join(summoner_name)

        if not self.is_valid_username(summoner_name):
            return

        summoner_info = await get_summoner_info(self.bot.session, summoner_name)
        if not summoner_info:
            return

        summoner_name = summoner_info['name']  # since $lol command is case insensitive and we want the real name
        elo_info = await get_league_info(self.bot.session, summoner_info['id'])
        elo_info = [elo for elo in elo_info if elo['queueType'] == 'RANKED_SOLO_5x5']
        solo_queue_info = elo_info[0] if elo_info else None
        recent_matches = await get_recent_matches(self.bot.session, summoner_info['accountId'])
        match_stats = await get_matches_stats(self.bot.session, recent_matches) if recent_matches else None
        summoner_matches_info = self.get_summoner_match_stats(match_stats, summoner_name) if match_stats else None

        await ctx.send(embed=self.create_embed(summoner_name,
                       description=self.build_description(summoner_info, solo_queue_info, summoner_matches_info)))