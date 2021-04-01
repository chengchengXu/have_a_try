# coding: utf-8

import asyncio
import websockets
import json
import random

reg_k = None


def handle(cmd):
    def handle_heartbeat(param):
        print(f'handle HEARTBEAT, {param}')
    def handle_put_log(param):
        print(f'handle LOG: ')
        print(*param, sep='\n')
    def handle_reg_k(param):
        global reg_k
        print(f'handle REG_K, {param}')
        reg_k = {'type': 'k', 'param': param}
    def handle_unreg_k(param):
        global reg_k
        print(f'handle UNREG_K, {param}')
        reg_k = None
    def handle_stop(param):
        print(f'handle STOP, {param}')
    def handle_default(param):
        print(f'handle DEFAULT silent')
    funcs_handle = {
        'heartbeat': handle_heartbeat,
        'put_log': handle_put_log,
        'reg_k': handle_reg_k,
        'unreg_k': handle_unreg_k,
        'stop': handle_stop,
    }
    func = funcs_handle.get(cmd['type'], handle_default)
    func(cmd['param'])
    return cmd


async def holder_user(ws, path):
    global reg_k
    print(f"in {path}")
    while True:
        await asyncio.sleep(random.randint(1, 2))
        if reg_k:
            await ws.send(json.dumps(reg_k))
        try:
            mesg = await asyncio.wait_for(ws.recv(), timeout=3)
            res = handle(json.loads(mesg))
            await ws.send(json.dumps(res))
        except asyncio.TimeoutError:
            print('recv time out')


start_server = websockets.serve(holder_user, "localhost", 25020)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
