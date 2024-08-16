from flask import Flask, render_template, url_for, request, redirect, jsonify
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import binascii, codecs
import time
import requests

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' ##
# db = SQLAlchemy(app)


@app.route('/donga/gookhwe/dummy', methods=['get'])
def test():
    
    objs={'xname':'test', 'xsubj':'test', 'xdesc':'test'}
    with open('dummy_text.txt', 'r', encoding='utf-8') as f:
        blob_scrol = f.read()
    # blob_scrol = codecs.decode(a, 'utf-8')
    # print(blob_scrol)
    article =blob_scrol.replace('\n','<BR>')

    # article = blob_scrol.strip().split('\n')

    # article = ''
    # for text0 in text_list:
    #     if text0[0] == '-':
    #         text0 = '<br><br>'+text0
    #     article += text0 + ' '
    # for article in cursor.fetchall()[::-1]:
    #     objs.append({
    #         'time0': article[0].strftime("%H:%M"),
    #         'title': codecs.decode(article[1], 'utf-8'),
    #         'press': article[2],
    #         'url': article[3],
    #         'ind': article[4],
    #         'writen': 'writen' if article[5] else 'None',
    #         'cp': article[6],
    #     })
    return render_template('sihwang.html', article= article, objs=objs)

#
# ## 요약작성 ##
# @app.route('/donga/dangbun/naver/write', methods = ['POST','GET'])
# def write():
#     if request.method == 'POST':
#         url = request.form['url']
#         press = request.form['press']
#         title = request.form['title']
#         ind = request.form['ind']
#         lead = giveme_lead(url, press, ind)
#         if '[속보]' in title:
#             text = f"@{press}/{title} {url}"
#         else:
#             text = f"@{press}/{title} = {lead} {url}"
#         return text
#
#
# ##실수로 들어왔을때 ##
# @app.route('/donga/dangbun/', methods = ['POST','GET'])
# def mistake_2_1():
#     return redirect('http://testbot.ddns.net:5234/donga/dangbun/')
#

if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    # with open('C:/stamp/port.txt', 'r') as f:
        # port = f.read().split(',')[0]  # 노트북 5232, 데스크탑 5231
        # port = port[0]
    # print(port)
    # host = '0.0.0.0'
    # if port == '5232':
    #     port ='5236'
    #     host = '172.30.1.58'
    #     host = '0.0.0.0'

    # elif port == '5231':
    port = '5236'
    host = '0.0.0.0'
    # port = 5233
    # 172.30.1.53
    # 0.0.0.0
    app.run(host=host, port=port, debug=True)
