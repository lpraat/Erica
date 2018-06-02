import asyncio
from os import getenv

LOL_KEY = getenv("LOLKEY")
lol_header = {'X-Riot-Token': LOL_KEY}

riot_api = "https://euw1.api.riotgames.com"
get_summoner_api = riot_api + "/lol/summoner/v3/summoners/by-name/"
get_league_api = riot_api + "/lol/league/v3/positions/by-summoner/"
get_all_matches_api = riot_api + "/lol/match/v3/matchlists/by-account/"
get_match_api = riot_api + "/lol/match/v3/matches/"


async def get_summoner_info(session, summoner_name):
    """
    Retrieves the league of legends info of a summoner.
    :param session: the aiohttp session.
    :param summoner_name: the summoner's name.
    :return: a dict containing the info.
    """
    async with session.request(url=get_summoner_api + summoner_name, method='get', headers=lol_header) as response:
        if response.status == 200:
            keys = ('id', 'accountId', 'summonerLevel', 'name')
            response_json = await response.json()
            response = dict((k, str(v)) for k, v in response_json.items() if k in keys)
            return response


async def get_league_info(session, summoner_id):
    """
    Retrieves the elo info of a summoner.
    :param session: the aiohttp session.
    :param summoner_id: the summoner's id.
    :return: a dict containing the info.
    """
    async with session.request(url=get_league_api + summoner_id, method='get', headers=lol_header) as response:
        if response.status == 200:
            return await response.json()


async def get_recent_matches(session, account_id):
    """
    Retrieves all the recent match ids of a summoner.
    :param session: the aiohttp session.
    :param account_id: the summoner's account id.
    :return: a list with all the ids as strings.
    """
    async with session.request(url=get_all_matches_api + account_id + "/recent", method='get',
                               headers=lol_header) as response:
        if response.status == 200:
            matches = await response.json()
            match_ids = [str(match['gameId']) for match in matches['matches']]
            return match_ids


async def get_match_stat(session, match_id):
    """
    Retrieves the stats of a lol match.
    :param session: the aiohttp session.
    :param match_id: the match id.
    :return: a dict containing the stats.
    """
    async with session.request(url=get_match_api + match_id, method='get', headers=lol_header) as response:
        if response.status == 200:
            return await response.json()


async def get_matches_stats(session, match_ids):
    """
    Retrieves the stats of a set of lol matches. The requests are done asynchronously.
    :param session: the aiohttp session.
    :param match_ids: the ids of the matches.
    :return: a list of dict containing the stats.
    """
    tasks = []

    for match_id in match_ids:
        tasks.append(asyncio.ensure_future(get_match_stat(session, match_id)))

    matches = await asyncio.gather(*tasks)
    return matches
