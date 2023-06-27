
import requests
import json


## a에 b를 넣음. 리스트 숫자는 10개 유지
def still_10(a,b):
    a=a[len(b):] + b
    return a




def gimme_wss(xcode, xcgcd):
    url =f'https://assembly.webcast.go.kr/main/service/live_play.asp?xcode={xcode}&xcgcd={xcgcd}'
    response = requests.get(url)
    contents = response.text
    json_data = json.loads(contents)
    xsami = json_data['xsami']
    return xsami