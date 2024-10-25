import requests
import json
url = "https://assembly.webcast.go.kr/main/service/live_list.asp"
response = requests.get(url)
contents=response.text
json_data=json.loads(contents)
print(json_data)