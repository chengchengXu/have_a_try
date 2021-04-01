# coding: utf-8

import asyncio
import websockets
import random
import datetime

async def hold_user(websocket, path):
    user = await websocket.recv()
    print(f"in {user}")

    count = 10
    while count:
        count -= 1
        await asyncio.sleep(random.randint(3, 10))
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        print(f"out {now}")

    # long time no user in should close the websocket
    # send data with some period

start_server = websockets.serve(hold_user, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()