import asyncio
import spacexpy
from datetime import datetime

spacex = spacexpy.SpaceX()
loop = asyncio.get_event_loop()


async def get_past_launches():
    query = {
        "query": {"date_utc": {
            "$lte": datetime.utcnow().isoformat()
        }},
        "options": {
            "sort": {
                "date_utc": "desc"
            },
            "limit": 200
        }
    }
    response = await spacex.launches(rawdata=True, query=query)
    return response.data['docs']


def get_last_launch_webcast_url():
    launches = loop.run_until_complete(get_past_launches())
    last = launches[0]
    webcast_url = last['links']['webcast']
    return webcast_url
