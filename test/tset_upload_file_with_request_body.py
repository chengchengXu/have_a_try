# coding:utf-8

import requests
import json


def main():
    path = "C:\\Users\\chengcheng.x\\Desktop\\import_user_config.csv"
    config = {
        "configID": 0,
        "configName": "string",
        "configs": {
            "cloudConfig": {
                "cpuTime": 0,
                "downloadFlow": 0,
                "memoryTime": 0
            },
            "execEnvConfig": {
                "bandwidth": 0,
                "cpuCount": 0,
                "diskSpace": 0,
                "memory": 0,
                "parallelCount": 0
            },
            "expmConfig": {
                "diskSpace": 0,
                "saveCount": 0
            },
            "fileConfig": {
                "diskSpace": 0,
                "fileCount": 0
            }
        }
    }

    # url = "http://139.9.49.148:9998/testimportconfigfile"
    url = "http://139.9.49.148:9998/config/import/batch/file"
    # url = "http://localhost:9998/testimportconfigfile"
    with open(path, mode='rb') as f:
        res = requests.post(
            url
            , data={'config': json.dumps(config)}
            , files={'files': f}
        )
    print(json.loads(res.content))
    print(1)


if __name__ == '__main__':
    main()
