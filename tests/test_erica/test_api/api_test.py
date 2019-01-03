import asyncio
import unittest

import aiohttp


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.session = aiohttp.ClientSession()

    def tearDown(self):
        self.session.close()
