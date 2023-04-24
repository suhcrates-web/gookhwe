import requests

url = 'wss://smiai.webcast.go.kr:8091/aistt/bokji'
temp = requests.get(url)
print(temp.content.decode())