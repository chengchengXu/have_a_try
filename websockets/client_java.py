# coding: utf-8

import requests
import asyncio
import websockets
import json
import random

# endpoint = 'localhost:8080'
endpoint = 'localhost:25010'


async def hello(session):
    # uri = f"ws://{endpoint}/socket/{session}"
    uri = f"ws://{endpoint}/websocket/{session}"
    async with websockets.connect(uri) as websocket:
        name = input("what's your name? ")

        # await websocket.send(name)
        # print(f"> {name}")

        GetTest = lambda: {'name': name, 'gender': random.choice(['female', 'male']), 'age': random.randint(13, 43),
                           'weight': random.normalvariate(120, 10),
                           # 'height': random.normalvariate(170, 5),
                           }
        theTest = GetTest()
        await websocket.send(json.dumps({'type': 'test', 'param': theTest}))
        print(f"> {theTest}")

        theTest = GetTest()
        await websocket.send(json.dumps({'type': 'test', 'param': theTest}))
        print(f"> {theTest}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello('fb8-41ce-8393'))

    # data = {
    #     'userId': '123',
    #     'strategyId': '345',
    #     'sessionInfo': '000',
    # }
    # rsp = requests.post(url=f'http://{endpoint}/dqt/session', headers={'Content-Type': 'application/json;charset=utf8'},
    #                     data=json.dumps(data))
    # # requests.post
    # if rsp.ok:
    #     rsp_content = json.loads(rsp.content)
    #     if rsp_content['errInfo'] is None or rsp_content['errInfo']['errCode'] == 0:
    #         asyncio.get_event_loop().run_until_complete(hello(rsp_content['data']))
    #     else:
    #         print('session request failed')
    # else:
    #     print('session request denied')
    #     rsp.raise_for_status()
