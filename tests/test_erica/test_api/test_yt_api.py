import json
import unittest

import aiohttp

from erica.api.yt_api import get_video_info, is_video_valid

import asyncio


class TestYoutubeAPI(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()

    def test_get_video(self):
        async def get_result():
            result = await get_video_info(self.session, "r7DQDrRwNgI")
            self.assertTrue(is_video_valid(result))

        self.loop.run_until_complete(get_result())

    def tearDown(self):
        self.session.close()
        self.loop.close()
