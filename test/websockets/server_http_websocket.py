# coding: utf-8

import sys
import time
import asyncio
import websockets
import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 25010
wsServerPort = 25020

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


def start_websocket_server():
    start_server = websockets.serve(holder_user, hostName, wsServerPort)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print('test')
        time.sleep(5)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        print('test end')


def start_http_server():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    if sys.argv[1] == 'http':
        start_http_server()
    elif sys.argv[1] == 'websocket':
        start_websocket_server()
