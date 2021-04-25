# coding: utf-8

import os
import asyncio
import websockets
import random
import datetime
import time
import tempfile


def create_huge_data(size):
    f = tempfile.TemporaryFile(mode='w+')
    f.seek(size)
    f.write('test end')
    f.seek(0)
    data = f.read()
    f.close()
    return data


async def hold_user(websocket, path):
    want = await websocket.recv()
    print(f"in {want}")

    count = 10
    while count:
        count -= 1
        await asyncio.sleep(random.randint(3, 10))
        # size = random.randint(1, int(want)) * 1024 * 1024
        size = random.randint(1, int(want))
        data = create_huge_data(size)
        await websocket.send(data)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        print(f"out {size} at {now}")

    # long time no user in should close the websocket
    # send data with some period

start_server = websockets.serve(hold_user, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
