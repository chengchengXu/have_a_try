# coding: utf-8

import asyncio
import websockets
import random
import json
import requests
import os


FILE_SERVER_ENDPOINT = ''
FILE_SERVER_ENDPOINT_LOCAL = '127.0.0.1'
FILE_SERVER_ENDPOINT_REMOTE = 'dqdata-alpha.digquant.com'
TOKEN = ''


TEST_TYPE = 0
TEST_TYPE_HTTP = 1
TEST_TYPE_WEBSOCKET = 2


def test_dx_file_server_download_file():
    import requests

    file_name = 'fileServer.zip'

    url = f"http://{FILE_SERVER_ENDPOINT}:8090/DownloadFile?fileName={file_name}"

    payload = {}
    headers = {
        'Cookie': f'DXdqdataSESSIONID={TOKEN}',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print file content
    # print(response.text)

    with open(file_name, 'wb') as f:
        f.write(response.content)
        print('download finished')

    if os.path.exists(file_name):
        os.remove(file_name)
        print('remote finished')


def test_dx_file_server_upload_file():
    import requests

    url = f"http://{FILE_SERVER_ENDPOINT}:8090/UploadFile"

    payload = {}
    files = [
        ('data', (
        'fileServer.zip', open('d:/Documents/WXWork/1688851085663467/Cache/File/2021-01/fileServer.zip', 'rb'),
        'application/zip'))
    ]
    headers = {
        'Cookie': f'DXdqdataSESSIONID={TOKEN}',
        # 'Content-Type': 'multipart/form-data',  // should not use that for requests will all 'boundary' into that
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    # response = requests.request("POST", url, data=payload, files=files)

    print(response.text)


def test_dx_file_server_upload_file_with_string():
    import requests
    import io
    import json

    a = {'a': 123, 'b': ['fff', 'vdfvdf', '231facvd'], 'c': {'c1': 'cc11', 'c2': 3939, 'c3': [123, 44, 556]}}

    f0 = io.StringIO(json.dumps(a))
    f1 = io.StringIO(json.dumps(a))
    f2 = io.StringIO(json.dumps(a))

    url = f"http://{FILE_SERVER_ENDPOINT}:8090/UploadFile"

    payload = {}
    files = [
        # ('data', ('abc/test.txt', f0)),
        ('data0', ('test.txt_0', f0)),
        ('data1', ('test.txt_1', f1)),
        ('data2', ('test.txt_2', f2)),
    ]
    headers = {
        'Cookie': f'DXdqdataSESSIONID={TOKEN}',
        # 'Content-Type': 'multipart/form-data',  // should not use that for requests will all 'boundary' into that
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    # response = requests.request("POST", url, data=payload, files=files)

    print(response.text)


def afm_file_system_upload_file():
    import requests

    url = "http://124.71.169.159:9999/upload"

    payload = {
        'uploadInfo': '{"userId":"0","parentId": "0","isForce": true,"fileContents": {"fileName": "test.csv","fileType": "file","filePath": "/","fileSize": "441","fileContents": []}}'
    }
    files = [
        ('files', ('test.csv', open('d:/Documents/test.csv', 'rb'), 'text/csv'))
    ]
    # headers = {
    #     'Content-Type': 'multipart/form-data'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response = requests.request("POST", url, data=payload, files=files)

    print(response.text)


async def with_websocket_server(url):
    count = 0
    async with websockets.connect(url) as websocket:
        while True:
            x = random.randint(0, 49)
            if not x:
                print('break that')
                break
            msg = f'the message with {x} 这是个中文'
            wb_msg = {'msgType': 'append', 'data': {'fileName': 'abc/test/logs', 'content': msg}}
            count += 1
            print(f'sending {count}')
            print(f'the message> {wb_msg}')
            await websocket.send(json.dumps(wb_msg))
            print(f'finish sending {count}')
            await asyncio.sleep(1)


def log_in():
    url = f"http://{FILE_SERVER_ENDPOINT}:8090/login"
    response = requests.post(url=url, json={"loginName":"yluo","loginType":"password","password":"x6321665","sessionId":"","verifyCode":""})
    # response = requests.request("post", url=url, data={"loginName":"yluo","loginType":"password","password":"x6321665","sessionId":"","verifyCode":""}, playloads=json.dumps({"loginName":"yluo","loginType":"password","password":"x6321665","sessionId":"","verifyCode":""}))
    temp = json.loads(response.content)
    global TOKEN
    TOKEN = json.loads(response.content)['data']['token']
    print(TOKEN)


def main():
    global TEST_TYPE
    global FILE_SERVER_ENDPOINT
    TEST_TYPE = TEST_TYPE_HTTP
    FILE_SERVER_ENDPOINT = FILE_SERVER_ENDPOINT_REMOTE
    if TEST_TYPE == TEST_TYPE_HTTP:
        log_in()
        test_dx_file_server_download_file()
        # afm_file_system_upload_file()
        test_dx_file_server_upload_file()
        test_dx_file_server_upload_file_with_string()
    elif TEST_TYPE == TEST_TYPE_WEBSOCKET:
        USE_DX_URI = True
        dx_uri = f"ws://{FILE_SERVER_ENDPOINT}:8091/open"
        sth_uri = f"ws://localhost:25020/ws/test/{random.randint(0, 100):03d}"
        asyncio.get_event_loop().run_until_complete(
            asyncio.wait([
                with_websocket_server(url=dx_uri if USE_DX_URI else sth_uri)
            ])
        )


if __name__ == '__main__':
    main()
