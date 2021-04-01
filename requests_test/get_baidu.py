import requests


def test_get_anything():
    # url = "http://www.baidu.com"
    url = 'https://www.huaweicloud.com'

    payload = {}
    # headers = {
    #   'Cookie': 'BIDUPSID=96FC53106F0BB078ED820F436920394A; PSTM=1606791130; BAIDUID=96FC53106F0BB0789564FE9ACC0F8243:FG=1; BDSVRTM=12; BD_HOME=1; H_PS_PSSID=1448_33058_33099_33100_32845_33198'
    # }

    # response = requests.request("GET", url, headers=headers, data = payload)
    # response = requests.request("GET", url, data = payload)
    # response = requests.get(url, headers={}, json={}, verify=False)
    response = requests.get(url, headers={}, json={})

    print(response.text.encode('utf8'))


def test_token():
    import requests

    url = "https://iam.cn-south-1.myhuaweicloud.com/v3/auth/tokens"

    payload = "{\r\n\t\"auth\": {\r\n\t\t\"identity\": {\r\n\t\t\t\"methods\": [\"password\"],\r\n\t\t\t\"password\": {\r\n\t\t\t\t\"user\": {\r\n\t\t\t\t\t\"name\": \"hw13258492\",\r\n\t\t\t\t\t\"password\": \"Dq20201020\",\r\n\t\t\t\t\t\"domain\": {\r\n\t\t\t\t\t\t\"name\": \"hw13258492\"\r\n\t\t\t\t\t}\r\n\t\t\t\t}\r\n\t\t\t}\r\n\t\t},\r\n\t\t\"scope\": {\r\n                \"project\": {\r\n                    \"name\": \"cn-east-3\"\r\n                }\r\n\t\t}\r\n\t}\r\n  }"
    headers = {
        'Content-Type': 'application/json;charset=utf8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


test_get_anything()