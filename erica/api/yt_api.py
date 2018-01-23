from os import getenv

YOUTUBE_KEY = getenv("YTKEY")
yt_api = f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_KEY}"


async def get_video_info(session, video_id):
    async with session.get(yt_api, params={'part': 'snippet', 'id': video_id}) as response:
        return await response.json()

def is_video_valid(video):
    return video['pageInfo']['totalResults'] == 1