# coding: utf-8

import asyncio
import websockets
import json
import random
import time

g_stop = False
g_heartbeat_recv = None


class SubAPIServer():
    _port = 'localhost:25020'
    _uri = ''
    _out_mesg = asyncio.Queue()
    # todo overdrive later


class DataSubAPIServer():
    _port = 'localhost:25020'
    _uri = ''
    _out_mesg = asyncio.Queue()

    @staticmethod
    async def loop(in_mesg):
        uri = f'ws://{DataSubAPIServer._port}{DataSubAPIServer._uri}'
        async with websockets.connect(uri) as ws:
            print(f'connection ready {__class__.__name__}')
            try:
                while not g_stop:
                    for _ in range(DataSubAPIServer._out_mesg.qsize()):
                        msg = await DataSubAPIServer._out_mesg.get()
                        await ws.send(json.dumps(msg))
                        DataSubAPIServer._out_mesg.task_done()
                    try:
                        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=2))
                        await in_mesg.put(msg)
                    except asyncio.TimeoutError as e:
                        # don't handle the timeout of recv
                        pass
            except Exception as e:
                print(e)
            except KeyboardInterrupt as k:
                print('user stop')
        print(f'stop {__class__.__name__}')


class RegK(DataSubAPIServer):
    _type = 'reg_k'

    @staticmethod
    def send(param):
        DataSubAPIServer._out_mesg.put_nowait({'type': RegK._type, 'param': param})


class UnregK(DataSubAPIServer):
    _type = 'unreg_k'

    @staticmethod
    def send(param):
        DataSubAPIServer._out_mesg.put_nowait({'type': UnregK._type, 'param': param})


class TradeSubAPIServer():
    _port = 'localhost:25020'
    _uri = ''
    _out_mesg = asyncio.Queue()

    @staticmethod
    async def loop(in_mesg):
        uri = f'ws://{TradeSubAPIServer._port}{TradeSubAPIServer._uri}'
        async with websockets.connect(uri) as ws:
            print(f'connection ready {__class__.__name__}')
            try:
                while not g_stop:
                    for _ in range(TradeSubAPIServer._out_mesg.qsize()):
                        msg = await TradeSubAPIServer._out_mesg.get()
                        await ws.send(json.dumps(msg))
                        TradeSubAPIServer._out_mesg.task_done()
                    try:
                        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=2))
                        if msg['type'] == 'k':
                            continue
                        await in_mesg.put(msg)
                    except asyncio.TimeoutError as e:
                        # don't handle the timeout of recv
                        pass
            except Exception as e:
                print(e)
            except KeyboardInterrupt as k:
                print('user stop')
        print(f'stop {__class__.__name__}')


class Account(TradeSubAPIServer):
    _type = 'ask_account'

    @staticmethod
    def send(param):
        TradeSubAPIServer._out_mesg.put_nowait({'type': Account._type, 'param': param})


class TaskSubAPIServer():
    _port = 'localhost:25020'
    _uri = ''
    _out_mesg = asyncio.Queue()

    @staticmethod
    async def loop(in_mesg):
        uri = f'ws://{TaskSubAPIServer._port}{TaskSubAPIServer._uri}'
        async with websockets.connect(uri) as ws:
            print(f'connection ready {__class__.__name__}')
            asyncio.create_task(HeartBeat.loop())
            try:
                while not g_stop:
                    for _ in range(TaskSubAPIServer._out_mesg.qsize()):
                        msg = await TaskSubAPIServer._out_mesg.get()
                        await ws.send(json.dumps(msg))
                        TaskSubAPIServer._out_mesg.task_done()
                    try:
                        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=2))
                        if msg['type'] == 'k':
                            continue
                        await in_mesg.put(msg)
                    except asyncio.TimeoutError as e:
                        # don't handle the timeout of recv
                        pass
            except Exception as e:
                print(e)
            except KeyboardInterrupt as k:
                print('user stop')
        print(f'stop {__class__.__name__}')


class PutLog(TaskSubAPIServer):
    _type = 'put_log'

    @staticmethod
    def send(param):
        TaskSubAPIServer._out_mesg.put_nowait({'type': PutLog._type, 'param': param})


class TaskStop(TaskSubAPIServer):
    _type = 'stop'

    @staticmethod
    def send(param):
        TaskSubAPIServer._out_mesg.put_nowait({'type': TaskStop._type, 'param': param})


class HeartBeat(TaskSubAPIServer):
    _type = 'heartbeat'

    @staticmethod
    async def loop():
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
            HeartBeat.send(random.randint(1000, 2000))
        print(f'stop {__class__.__name__}')

    @staticmethod
    def send(param):
        TaskSubAPIServer._out_mesg.put_nowait({'type': HeartBeat._type, 'param': param})


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
        {'type': RegK._type,
         'param': random.choices([{'market': 'sse', 'symbol': '600001'}, {'market': 'szse', 'symbol': '000333'},
                                  {'market': 'shfe', 'symbol': 'ag.000001'}], k=random.randint(1, len(logs)))},
        {'type': UnregK._type, 'param': {'market': 'sse', 'symbol': '600001'}},
        {'type': Account._type, 'param': {'id': 8474665521}},
        {'type': PutLog._type, 'param': random.choices(logs, k=random.randint(1, len(logs)))},
        {'type': TaskStop._type, 'param': time.ctime(time.time())}
    ]
    return random.choices(options, weights=[30, 3, 17, 45, 0])[0]


async def generate_cmd():
    global g_stop
    cmd_send = {
        RegK._type: RegK.send,
        UnregK._type: UnregK.send,
        Account._type: Account.send,
        PutLog._type: PutLog.send,
        TaskStop._type: TaskStop.send,
    }
    while not g_stop:
        await asyncio.sleep(random.randint(1, 2))
        cmd = get_one_cmd()
        cmd_send[cmd['type']](cmd['param'])
    print('stop generate_cmd')


async def loop(in_mesg):
    global g_stop
    while not g_stop:
        await asyncio.sleep(random.randint(1, 2))
        for _ in range(in_mesg.qsize()):
            mesg = in_mesg.get_nowait()
            handle(mesg)
            in_mesg.task_done()
    print('stop loop')


def main():
    in_mesg = asyncio.Queue()
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            loop(in_mesg),
            DataSubAPIServer.loop(in_mesg),
            TradeSubAPIServer.loop(in_mesg),
            TaskSubAPIServer.loop(in_mesg),
            generate_cmd(),
        ])
    )


if __name__ == "__main__":
    main()
