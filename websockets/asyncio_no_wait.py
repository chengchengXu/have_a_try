# coding: utf-8

import os
import asyncio
import random


async def loop_no_wait(n):
    t = []
    for i in range(int(n)):
        t.append(random.randint(0, i))
    print(f'loop_no_wait: {len(t) + random.randint(0, n)}')
    return t


async def loop_with_wait(n):
    i = int(n)
    t = []
    while i > 0:
        t.append(random.randint(0, i))
        i = int(i / 10)
        print(f'loop_with_wait: {t[-1]}')
        # await asyncio.sleep(random.randint(1, 4))
    print(f'loop_with_wait: nothing')


def main():
    n = 1e6
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            loop_no_wait(n),
            loop_with_wait(n)
        ])
    )


if __name__ == '__main__':
    main()
