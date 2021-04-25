# coding: utf-8

import asyncio, random


async def rnd_sleep(t):
    await asyncio.sleep(t * random.random() * 2)


async def producer(no, queue):
    # async def producer(queue):
    while True:
        token = random.random()
        print(f'{no} produced {token}')
        # print(f'produced {token}')
        if token < .05:
            print(f'{no} want to finish {token}')
            break
        await queue.put(token)
        await rnd_sleep(.1)


async def consumer(no, queue):
    # async def consumer(queue):
    while True:
        token = await queue.get()
        await rnd_sleep(.3)
        queue.task_done()
        # print(f'consumed {token}')
        print(f'{no} consumed {token}')


async def main():
    queue = asyncio.Queue()

    producers = [asyncio.create_task(producer(no, queue)) for no in range(3)]
    consumers = [asyncio.create_task(consumer(no, queue)) for no in range(10)]
    # producers = [asyncio.create_task(producer(queue)) for _ in range(3)]
    # consumers = [asyncio.create_task(consumer(queue)) for _ in range(10)]

    await asyncio.gather(*producers)
    print('---- done producing')

    await queue.join()
    for c in consumers:
        c.cancel()


asyncio.run(main())
