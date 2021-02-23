import random
from time import sleep
import asyncio

def task(pid):
    sleep(random.randint(0,2)*0.001)
    print('Task %s done' % pid)


async def task_coro(pid):
    await asyncio.sleep(random.randint(0,2)*0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1,10):
        task(i)


async def asynchronous():
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1,10)]
    await asyncio.wait(tasks)


print('synchronous:')
synchronous()

ioloop = asyncio.get_event_loop()
print('asynchronous:')
ioloop.run_until_complete(asynchronous())
ioloop.close()