import time
import urllib.request
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


def fetch_sync(pid):
    print('Fetch sync process {} started'.format(pid))
    start = time.time()
    response = urllib.request.urlopen(URL)
    datetime = response.getheader('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(pid, datetime, time.time()-start))

    return datetime


async def fetch_async(pid, session):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    async with session.get(URL) as response:
        datetime = response.headers.get('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(pid, datetime, time.time() - start))

    return datetime


def synchronous():
    start = time.time()
    for i in range(1,MAX_CLIENTS+1):
        fetch_sync(i)
    print('Process took: {:.2f} seconds'.format(time.time() - start))

async def asynchronous():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(
            fetch_async(pid, session)) for pid in range(1, MAX_CLIENTS + 1)]
        await asyncio.gather(*tasks)
    print('Process took: {:.2f} seconds'.format(time.time() - start))

print('synchronous:')
synchronous()

print('asynchronous:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())