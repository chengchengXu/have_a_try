# coding: utf-8

import asyncio
import websockets
from time import sleep
import random
import datetime


msg = []

async def with_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("what's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        while True:
            data = await websocket.recv()
            print(f"> recv {data} at {datetime.datetime.now()}")
            msg.append(data)


async def loop():
    count = 40
    while count:
        count -= 1
        await asyncio.sleep(random.randint(2, 4))
        # sleep(random.randint(2, 4))  # this will block others
        if len(msg):
            print(f"> handle the data {msg.pop(0)} at {datetime.datetime.now()}")
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
