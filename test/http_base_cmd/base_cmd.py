# coding: utf-8

import requests
import json


class HttpBaseCmd:
    def __init__(self, url="Need to add url", mode="get", headers=None, pack=None,
                 unpack=None, checker=None):
        self._url = url
        self._mode = mode
        self._pack = pack if pack else json.dumps
        self._unpack = unpack if unpack else json.loads
        self._checker = checker if checker else HttpBaseCmd._checker
        self._headers = headers if headers else {'Content-Type': 'application/json;charset=UTF-8'}

    def send(self, **kwargs):
        param = ''
        rsp = ''
        result = ''
        try:
            param = self._pack(kwargs)
        except:
            print(f"pack {self.__class__.__name__} fail")
            raise
        try:
            rsp = requests.request(self._mode, self._url, headers=self._headers, data=param)
        except:
            print(f"request {self.__class__.__name__} fail")
            raise
        if not rsp.ok:
            rsp.raise_for_status()
        try:
            result = self._unpack(rsp.content)
        except:
            print(f"unpack {self.__class__.__name__} fail")
            raise
        return self._checker(result)

    @staticmethod
    def _checker(result):
        if result['errCode']:
            raise Exception(result['errMsg'])
        return result['data']