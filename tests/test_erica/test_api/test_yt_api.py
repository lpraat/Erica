import asyncio

from erica.api.yt_api import get_video_info, is_video_valid
from tests.test_erica.test_api.api_test import ApiTest


class TestYoutubeAPI(ApiTest):

    def test_get_video(self):
        async def get_result():
            result = await get_video_info(self.session, "r7DQDrRwNgI")
            self.assertTrue(is_video_valid(result))

            result = await get_video_info(self.session, "invalidId")
            self.assertFalse(is_video_valid(result))

        asyncio.get_event_loop().run_until_complete(get_result())





