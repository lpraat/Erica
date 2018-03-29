import asyncio

from erica.api.lol_api import get_summoner_info, get_league_positions, get_matches_stats, get_recent_matches
from erica.cogs.lol_stats import LolStats
from tests.test_erica.test_api.api_test import ApiTest


class TestLolApi(ApiTest):

    def test_summoner_name_regex(self):
        lolstats = LolStats(None)
        self.assertTrue(lolstats.is_valid_username("soli1411"))
        self.assertTrue(lolstats.is_valid_username("012345678"))
        self.assertFalse(lolstats.is_valid_username("0sorlac@@0"))

    def test_get_summoner_info(self):
        async def get_result():
            lolstats = LolStats(None)
            result = await get_summoner_info(self.session, "0sorlac0")
            self.assertIsNotNone(result)

            account_id = result['accountId']
            summoner_id = result['id']
            summoner_name = result['name']

            result = await get_league_positions(self.session, summoner_id)
            self.assertIsNotNone(result)

            match_ids = await get_recent_matches(self.session, account_id)

            if match_ids:

                matches_stats = await get_matches_stats(self.session, match_ids)

                if matches_stats:
                    self.assertIsNotNone(lolstats.kda(lolstats.get_summoner_match_stats(matches_stats, summoner_name)))

        asyncio.get_event_loop().run_until_complete(get_result())