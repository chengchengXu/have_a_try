# coding: utf-8

import requests
import json


def get_file_info_by_path(path):
    uri = f"/getFileInfoByPath"
    end_point = f"124.70.142.108:9999"
    url = f'http://{end_point}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'}
    data = {"filePath": path, "userId": "0"}

    res = requests.post(url, data=json.dumps(data), headers=headers)
    res_data = json.loads(res.content)
    if res_data['errCode'] == 0 and res_data['data'] is not None:
        return res_data['data']['fileId']
    else:
        print(res_data['errMsg'])
        return None


def main():
    file_id = get_file_info_by_path(f"afm/DataSet/001001ScrewThreadSteel.csv")
    print(file_id)


if __name__ == '__main__':
    main()
