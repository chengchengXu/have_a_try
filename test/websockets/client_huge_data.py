# coding: utf-8

import asyncio
import websockets
from time import sleep
import random
import datetime


msgs = []

async def with_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        want = input("what's your want size? ")

        await websocket.send(want)
        print(f"> {want}")

        while True:
            data = await websocket.recv()
            print(f"> recv {data[:10]} at {datetime.datetime.now()}")
            msgs.append(data)


async def loop():
    count = 40
    while count:
        count -= 1
        await asyncio.sleep(random.randint(2, 4))
        if len(msgs):
            print(f"> handle the data {msgs.pop(0)[:10]} at {datetime.datetime.now()}")
        else:
            print(f"> skip at {datetime.datetime.now()}")


def main():
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            with_server(),
            loop()
        ])
    )


if "__main__" == __name__:
    main()
