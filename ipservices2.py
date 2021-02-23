from collections import namedtuple
import time
import aiohttp
import asyncio
import traceback
from concurrent.futures import FIRST_COMPLETED

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


async def fetch_ip(service, session):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    try:
        response = await session.get(service.url)
    except:
        return "{} is unrensponsive".format(service.name)
    json_response = await response.json()
    ip = json_response[service.ip_attr]
    response.close()
    return '{} finished with result: {}, took: {:.2f} seconds'.format(service.name, ip, time.time() - start)

async def asynchronous():
    session = aiohttp.ClientSession()
    futures = [fetch_ip(service, session) for service in SERVICES]
    done, _ = await asyncio.wait(futures)


    for future in done:
        try:
            print(future.result())
        except:
            print("Unexpected error: {}".format(traceback.format_exc()))

    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(asynchronous())


