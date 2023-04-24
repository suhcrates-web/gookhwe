# import requests
# import json
# url = "https://assembly.webcast.go.kr/main/service/live_list.asp"
# response = requests.get(url)
# print(json.loads(response.content))
import re
a = '//thumb.webcast.go.kr/api/thumbnail/bokji'

b = re.search(r'(?<=/)[^/]+$',a)
# b = re.search(r'/(\w+)$',a)
print(b[0])

