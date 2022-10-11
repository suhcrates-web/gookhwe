from bs4 import BeautifulSoup
import math
from datetime import datetime

import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
urllib3.disable_warnings()

url ='https://assembly.webcast.go.kr/main/service/live_list.asp'
# url ='https://assembly.webcast.go.kr/main/service/live_list.asp?vv=1659601968&'

data = {
    'vv':str(math.floor(datetime.now().timestamp()))
}
header = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'ASPSESSIONIDQUDCQTRR=MIFLJJKBOEGBGHHDBNCLIEOP; _ga=GA1.1.1382456315.1659598949; player_opt=0; ASPSESSIONIDQUSTDDQB=CGFOBMIBFLKNOEJDAGJIEKAO; ASPSESSIONIDQUTSDDTA=NPGEBKIBBENMHCMIGONOGCNJ; _ga_QEPEGVC0VX=GS1.1.1659600816.2.1.1659603842.0',
'Host': 'assembly.webcast.go.kr',
'Referer': 'https://assembly.webcast.go.kr/main/',
'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
}

# header = {
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Cookie': 'ASPSESSIONIDQUDCQTRR=MIFLJJKBOEGBGHHDBNCLIEOP; _ga=GA1.1.1382456315.1659598949; player_opt=0; ASPSESSIONIDQUSTDDQB=CGFOBMIBFLKNOEJDAGJIEKAO; ASPSESSIONIDQUTSDDTA=NPGEBKIBBENMHCMIGONOGCNJ; _ga_QEPEGVC0VX=GS1.1.1659600816.2.1.1659603842.0',
# 'Host': 'assembly.webcast.go.kr',
# 'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-ch-ua-platform': '"Windows"',
# 'Sec-Fetch-Dest': 'document',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-Site': 'none',
# 'Sec-Fetch-User': '?1',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
# }

temp = requests.get(url, headers=header, data=data)
# print(temp.content)
temp = BeautifulSoup(temp.content, 'html.parser')
print(temp)