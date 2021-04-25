# coding: utf-8

import asyncio
import websockets
import json
import random
import time

g_stop = False
g_heartbeat_recv = None
g_in_mesg = asyncio.Queue()
g_out_mesg = asyncio.Queue()


def handle(cmd):
    def handle_default(param):
        print(f'handle DEFAULT silent')

    def handle_k(param):
        print(f'handle K, {param}')

    def handle_heartbeat(param):
        global g_heartbeat_recv
        print(f'handle HEARTBEAT recv, {param}')
        g_heartbeat_recv = time.time()

    def handle_stop(param):
        global g_stop
        g_stop = True

    funcs_handle = {
        'k': handle_k,
        'heartbeat': handle_heartbeat,
        'stop': handle_stop
    }
    func = funcs_handle.get(cmd['type'], handle_default)
    func(cmd['param'])


def get_one_cmd():
    logs = ['first one log', 'second log', 'you get the third one', 'log for 4']
    options = [
        {'type': 'reg_k',
         'param': random.choices([{'market': 'sse', 'symbol': '600001'}, {'market': 'szse', 'symbol': '000333'},
                                  {'market': 'shfe', 'symbol': 'ag.000001'}], k=random.randint(1, len(logs)))},
        {'type': 'unreg_k', 'param': {'market': 'sse', 'symbol': '600001'}},
        {'type': 'ask_account', 'param': {'id': 8474665521}},
        {'type': 'put_log', 'param': random.choices(logs, k=random.randint(1, len(logs)))},
        {'type': 'stop', 'param': time.ctime(time.time())}
    ]
    return random.choices(options, weights=[30, 3, 17, 20, 30])[0]


async def with_server(in_mesg=g_in_mesg, out_mesg=g_out_mesg):
    global g_stop
    uri = 'ws://localhost:25010'
    lose_time = 0
    while not g_stop:
        async with websockets.connect(uri) as ws:
            name = input('your name? ')

            await ws.send(name)
            print(f'connection ready')

            try:
                while not g_stop:
                    # await asyncio.sleep(random.randint(1, 3))
                    for _ in range(out_mesg.qsize()):
                        mesg = await out_mesg.get()
                        await ws.send(json.dumps(mesg))
                        out_mesg.task_done()
                    try:
                        mesg = await asyncio.wait_for(ws.recv(), timeout=3)
                        await in_mesg.put(json.loads(mesg))
                    except asyncio.TimeoutError:
                        print('time out')
            except Exception as e:
                print(e)
        lose_time += 1
        if lose_time > 3:
            g_stop = True
            print('lose too many times connection')
    print('stop with_websocket_server')


async def generate_cmd(in_mesg=g_in_mesg, out_mesg=g_out_mesg):
    global g_stop
    while not g_stop:
        await asyncio.sleep(random.randint(2, 5))
        await out_mesg.put(get_one_cmd())
    print('stop generate_cmd')


async def loop(in_mesg=g_in_mesg, out_mesg=g_out_mesg):
    global g_stop
    while not g_stop:
        await asyncio.sleep(random.randint(1, 2))
        for _ in range(in_mesg.qsize()):
            mesg = await in_mesg.get()
            handle(mesg)
            in_mesg.task_done()
    print('stop loop')


async def heartbeat(in_mesg=g_in_mesg, out_mesg=g_out_mesg):
    global g_stop, g_heartbeat_recv
    g_heartbeat_recv = time.time()
    lose_count = 0
    while not g_stop:
        sleep_time = 10 - int(time.time() - g_heartbeat_recv)
        lose_count = lose_count + 1 if sleep_time <= 0 else 0
        if lose_count >= 3:
            g_stop = True
            print('heartbeat meet max lose time')
            break
        await asyncio.sleep(max(3, sleep_time))
        await out_mesg.put({'type': 'heartbeat', 'param': random.randint(1000, 2000)})
    print('stop heartbeat')


def main():
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            with_server(),
            loop(),
            heartbeat(),
            generate_cmd(),
        ])
    )


if __name__ == "__main__":
    main()
