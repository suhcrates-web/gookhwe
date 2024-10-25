import requests
from bs4 import BeautifulSoup

url = 'https://assembly.webcast.go.kr/main/player.asp?xcode=39&xcgcd=DCM000039213980101&'
temp = requests.get(url)
temp = BeautifulSoup(temp.content, 'html.parser')
print(temp)

