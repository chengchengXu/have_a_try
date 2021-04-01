import requests

url = "http://124.71.169.159:22088/spending/list/users"

payload="[213]"
headers = {
  'Content-Type': 'application/json;charset=UTF-8'
}
x = {'data': "[213]", 'headers': {'Content-Type': 'application/json;charset=UTF-8'}}
# x = {'data': "[213]"}
response = requests.request("POST", url, **x)

# response = requests.request("POST", url, headers=headers, **x)

print(response.text)
