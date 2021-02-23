from collections import namedtuple
import time
import aiohttp
import asyncio
import traceback
import random
from concurrent.futures import FIRST_COMPLETED

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)

DEFAULT_TIMEOUT = 0.01


async def fetch_ip(service, session):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    await asyncio.sleep(random.randint(1,3)*0.1)
    try:
        response = await session.get(service.url)
    except:
        return "{} is unrensponsive".format(service.name)
    json_response = await response.json()
    ip = json_response[service.ip_attr]
    response.close()
    print('{} finished with result: {}, took: {:.2f} seconds'.format(service.name, ip, time.time() - start))
    return ip

async def asynchronous(timeout):
    session = aiohttp.ClientSession()
    response = {"message": "Result from asynchronous.",
                "ip": "not available"}

    futures = [fetch_ip(service, session) for service in SERVICES]
    done, pending = await asyncio.wait(futures, timeout=timeout, return_when=FIRST_COMPLETED)

    for future in pending:
        future.cancel()

    for future in done:
        response['ip'] = future.result()

    print(response)

    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(asynchronous(0.5))


