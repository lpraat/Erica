from os import getenv

FORTNITE_KEY = getenv('FNKEY')
fornite_api = 'https://api.fortnitetracker.com/v1/profile/pc/'
fornite_header = {'TRN-Api-Key': FORTNITE_KEY}


async def get_player_info(session, nickname):
    """
    Gets the fortnite stats of a player.
    :param session: the aiohttp session.
    :param nickname: the player's nickname.
    :return: a dict containing the stats.
    """
    async with session.request(url=fornite_api + nickname, method='get', headers=fornite_header) as response:
        if response.status == 200:  # note: this api returns 200 even if a resource is not found...
            return await response.json()
