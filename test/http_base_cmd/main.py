# coding: utf-8

from test_cmd import SearchUserListCmd
from test_cmd import NotebookTaskListByUserID

if "__main__" == __name__:
    print(SearchUserListCmd.send('2963', 1, showItem=50))
    # print(NotebookTaskListByUserID.send([13151]))
    print(NotebookTaskListByUserID.send(users=[13151]))
