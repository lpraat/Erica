from os import getenv

YOUTUBE_KEY = getenv('YTKEY')
yt_api = f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_KEY}"


async def get_video_info(session, video_id):
    """
    Retrieves the video info from the youtube API using an aiohttp session.
    :param session: the aiohttp session.
    :param video_id: the id of the video.
    :return: a dict containing the info.
    """
    async with session.get(yt_api, params={'part': 'snippet', 'id': video_id}) as response:
        if response.status == 200:
            return await response.json()


def is_video_valid(video):
    """
    Checks if a video is valid by looking at the video info.
    :param video: the dict with the info of the video.
    :return: true if the video is valid false otherwise.
    """
    return video['pageInfo']['totalResults'] == 1
