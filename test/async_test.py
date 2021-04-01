# coding: utf-8

import asyncio
import random
import traceback


async def test_print_1(c):
    print(f"test_print_1: {random.randint(0, 100)}")
    c['1'] = random.randint(1, 10)
    await asyncio.sleep(1)


async def test_print_2(c):
    print(f"test_print_2: {random.randint(0, 100)}")
    print(c['1'] if c.get('1') else None)
    await asyncio.sleep(1)


async def test_print_3(c):
    print(f"test_print_3: {random.randint(0, 100)}")
    c['3'] = random.randint(1, 10)
    await asyncio.sleep(1)


async def test_print_4(c):
    print(f"test_print_4: {random.randint(0, 100)}")
    print(c['3'] if c.get('3') else None)
    await asyncio.sleep(1)


async def run_transmit_config():
    config = {
        'begin': random.randint(-1, 1)
    }
    tests = [
        test_print_1(config),
        test_print_2(config),
        test_print_3(config),
        test_print_4(config),
    ]
    random.shuffle(tests)
    for t in tests:
        await t
    print(config)


def test_order_of_wait_together():
    config = {
        'begin': random.randint(-1, 1)
    }
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            test_print_1(config),
            test_print_2(config),
            test_print_3(config),
            test_print_4(config),
        ])
    )


def test_transmit_config():
    asyncio.get_event_loop().run_until_complete(
        run_transmit_config()
    )


async def loop_print_1(msgs: asyncio.Queue):
    max_finish_count = 5
    while max_finish_count:
        if msgs.qsize():
            max_finish_count -= 1
            x = await msgs.get()
            msgs.task_done()
            if x == 1:
                # add loop
                asyncio.ensure_future(loop_print_2(msgs), loop=asyncio.get_event_loop())
                print(f'try again at {max_finish_count}')
        print(f'loop_print_1: {random.randint(1, 100)}')
        await asyncio.sleep(.1)


async def loop_print_2(msgs: asyncio.Queue):
    loop_count = 5
    while loop_count:
        loop_count -= 1
        print(f'loop_print_2: {random.randint(1, 100)}')
        await asyncio.sleep(.1)
    await msgs.put(1)


def test_add_task_to_event_loop():
    msgs = asyncio.Queue()
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            loop_print_1(msgs),
            loop_print_2(msgs),
        ])
    )


async def print_error_cross_async(config, e):
    await asyncio.sleep(1)
    print(traceback.format_exc())
    print('in print_error_cross_async for', config)
    print(e)


async def traceback_cross_async(config):
    try:
        x=1/0
    except Exception as e:
        await print_error_cross_async(config, e)


def test_traceback_cross_async_function():
    config = {
        'begin': random.randint(-1, 1)
    }
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            test_print_1(config),
            test_print_2(config),
            traceback_cross_async(config),
        ])
    )


if __name__ == "__main__":
    # test_order_of_wait_together()
    # test_transmit_config()
    # test_add_task_to_event_loop()
    test_traceback_cross_async_function()

    print("done")
