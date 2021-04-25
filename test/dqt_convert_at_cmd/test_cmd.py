# coding: utf-8

from base_cmd import HttpBaseCmd
import json


class TestServerCmd(HttpBaseCmd):
    _endpoint = 'alpha.digquant.com.cn:38080'

    def __init__(self, uri, **kwargs):
        super().__init__(url=f"http://{TestServerCmd._endpoint}{uri}", **kwargs)


class SearchUserListCmd(TestServerCmd):
    _uri = '/user/search'

    def __init__(self):
        super().__init__(uri=SearchUserListCmd._uri, mode="post")

    @staticmethod
    def send(keyword, pageIndex, **kwargs):
        if not hasattr(SearchUserListCmd, "cmd"):
            SearchUserListCmd.cmd = SearchUserListCmd()
        return super(SearchUserListCmd, SearchUserListCmd.cmd).send(keyword=keyword, pageIndex=pageIndex, **kwargs)


class JupyterHubServerCmd(HttpBaseCmd):
    # _endpoint = "124.70.142.108:2208"
    _endpoint = "124.70.142.108:22088"

    def __init__(self, uri, **kwargs):
        super().__init__(url=f"http://{JupyterHubServerCmd._endpoint}{uri}", **kwargs)
        # super().__init__(url=f"http://{TestServerCmd._endpoint}{uri}", **kwargs)


class NotebookTaskListByUserID(JupyterHubServerCmd):
    _uri = '/spending/list/users'

    def __init__(self):
        super().__init__(uri=NotebookTaskListByUserID._uri, mode="post", pack=NotebookTaskListByUserID.pack)

    @staticmethod
    def send(**kwargs):
        if not hasattr(NotebookTaskListByUserID, "cmd"):
            NotebookTaskListByUserID.cmd = NotebookTaskListByUserID()
        return super(NotebookTaskListByUserID, NotebookTaskListByUserID.cmd).send(**kwargs)

    @staticmethod
    def pack(kwargs):
        return json.dumps(kwargs['users'])