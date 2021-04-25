import requests

url = "https://iam.cn-south-1.myhuaweicloud.com/v3/auth/tokens"

payload="{\r\n\t\"auth\": {\r\n\t\t\"identity\": {\r\n\t\t\t\"methods\": [\"password\"],\r\n\t\t\t\"password\": {\r\n\t\t\t\t\"user\": {\r\n\t\t\t\t\t\"name\": \"hw13258492\",\r\n\t\t\t\t\t\"password\": \"Dq20201020\",\r\n\t\t\t\t\t\"domain\": {\r\n\t\t\t\t\t\t\"name\": \"hw13258492\"\r\n\t\t\t\t\t}\r\n\t\t\t\t}\r\n\t\t\t}\r\n\t\t},\r\n\t\t\"scope\": {\r\n\t\t\t\"domain\": {\r\n\t\t\t\t\"name\": \"hw13258492\"\r\n\t\t\t}\r\n\t\t}\r\n\t}\r\n  }"
headers = {
  'Content-Type': 'application/json;charset=utf8',
  'Cookie': 'HWWAFSESID=77fa97f18e6595ee97; HWWAFSESTIME=1608188573994'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
