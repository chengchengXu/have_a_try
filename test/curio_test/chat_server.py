# coding: utf-8

from curio import run, spawn, TaskGroup, Queue, tcp_server

messages = Queue()
subscribers = set()


async def dispatcher():
    while True:
        msg = await messages.get()
        for q in subscribers:
            await q.put(msg)


async def publish(msg):
    await messages.put(msg)


# Task that writes chat messages to clients
async def outgoing(client_stream):
    queue = Queue()
    try:
        subscribers.add(queue)
        while True:
            name, msg = await queue.get()
            await client_stream.write(name + b': ' + msg)
    finally:
        subscribers.discard(queue)


# Task that reads chat messages and publishs them
async def incoming(client_stream, name):
    async for line in client_stream:
        await publish((name, line))


async def chat_handler(client, addr):
    print('Connection from', addr)
    async with client:
        client_stream = client.as_stream()
        await client_stream.write(b'Your name: ')
        name = (await client_stream.readline()).strip()
        await publish((name, b'joined\n'))

        async with TaskGroup(wait=any) as workers:
            await workers.spawn(outgoing, client_stream)
            await workers.spawn(incoming, client_stream, name)

        await publish((name, b'has gone away\n'))

    print('Connection closed')


async def chat_server(host, port):
    async with TaskGroup() as g:
        await g.spawn(dispatcher)
        await g.spawn(tcp_server, host, port, chat_handler)


if __name__ == '__main__':
    # test
    # bash: nc localhost 25000
    # cmd: telnet 127.0.0.1 25000
    run(chat_server("", 25000))
