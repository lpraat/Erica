import asyncio
from erica.api.fn_api import get_player_info
from tests.test_erica.test_api.api_test import ApiTest


class TestFortniteApi(ApiTest):

    def test_get_player_info(self):
        async def get_result():
            result = await get_player_info(self.session, "Lu Xiaojun")
            self.assertTrue('error' not in result)

            result = await get_player_info(self.session, ".3423£$£43$£3???!1!!!1!")
            self.assertTrue('error' in result)

        asyncio.get_event_loop().run_until_complete(get_result())

