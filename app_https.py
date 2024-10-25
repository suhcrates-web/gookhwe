from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_cors import CORS
from datetime import date, datetime, timedelta
from database import config
import codecs
import mysql.connector
import re

app = Flask(__name__)
CORS(app)

@app.route('/donga/', methods = ['POST', 'GET'])
def main():
    today0 = date.today()
    return redirect(f'/donga/gookhwe/{today0}')

@app.route('/donga/gookhwe/', methods = ['POST','GET'])
def mistake_2_1():
    today0 = date.today()
    return redirect(f'/donga/gookhwe/{today0}')

@app.route('/donga/gookhwe/<date0>', methods=['get'])
def index(date0):
    # 4일 전부터는 DB에 데이터가 없으므로 오늘로 redirect
    input_date = datetime.strptime(date0, '%Y-%m-%d').date()
    today0 = date.today()
    four_days_ago = today0 - timedelta(days=4)
    if input_date <= four_days_ago or input_date > today0:
        return redirect(f'/donga/gookhwe/{today0}')
    
    # DB에 날짜가 있는 경우
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        f"""
        select xcode, xsubj, xname, xdesc, content
        from gookhwe_stuffs.live_list
        where date0="{date0}"
        """
    )
    date_split = date0.split('-')
    date_reform = str(date_split[1]) + '월 ' + str(date_split[2]) + '일'
    objs = []
    for temp in cursor.fetchall():
        content = temp[4]
        active = "True" if content else "False"
        cleaned_xsubj = re.sub(r'\[\d{1,2}:\d{2}\]', '', temp[1]).strip() # xsubj에서 시간 형식을 제거
        objs.append({'xcode':temp[0], 'xsubj':cleaned_xsubj, 'xname':temp[2], 'xdesc':temp[3], 'date0':date0, 'active':active})
    return render_template('bot_v3.html', objs=objs, date_reform=date_reform)


@app.route('/donga/gookhwe/<date0>/<xcode0>', methods=['get'])
def test(xcode0, date0):
    # date0에 대한 오류 처리
    input_date = datetime.strptime(date0, '%Y-%m-%d').date()
    today0 = date.today()
    four_days_ago = today0 - timedelta(days=4)
    if input_date <= four_days_ago or input_date > today0:
        return redirect(f'/donga/gookhwe/{today0}')

    date_split = date0.split('-')
    date_reform = str(date_split[1]) + '월 ' + str(date_split[2]) + '일'
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    objs = []
    cursor.execute(
        f"""
        select content, xname, xsubj, xdesc
        from gookhwe_stuffs.live_list
        where xcode='{xcode0}' and date0="{date0}"
        """
    )
    temp =  cursor.fetchall()[0]
    cursor.close()

    # 전체보기를 위해 리스트 가져오는 부분
    cursor = db.cursor()
    objs_list = []
    cursor.execute(
        f"""
        select xsubj, xname, xdesc, content, xcode
        from gookhwe_stuffs.live_list
        where date0="{date0}"
        """
    )
    for temp2 in cursor.fetchall():
        content = temp2[3]
        active = "True" if content else "False"
        cleaned_xsubj = re.sub(r'\[\d{1,2}:\d{2}\]', '', temp2[0]).strip()
        objs_list.append({'xsubj':cleaned_xsubj, 'xname': temp2[1], 'xdesc': temp2[2], 'active':active, 'xcode': temp2[4]})
    db.close()
    a = temp[0]
    objs={'xname':temp[1], 'xsubj':re.sub(r'\[\d{1,2}:\d{2}\]', '', temp[2]).strip(), 'xdesc':temp[3]}
    if a==None:
        blob_scrol = "데이터 없음 (개의 전이거나 수집 가능 대상 아님)"
    else:
        blob_scrol = codecs.decode(a, 'utf-8')
    article =blob_scrol.replace('\n','<BR>')
    key0=date0.replace('-', '') + '_' + xcode0
    return render_template('sihwang.html', article= article, objs=objs, live_key=key0, objs_list=objs_list, date0=date0, date_reform=date_reform)

# 당일 리스트 조회 및 업데이트를 위한 API
@app.route('/donga/gookhwe/<date0>/list', methods=['GET'])
def today_list(date0):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    objs_list = []
    cursor.execute(
        f"""
        select xsubj, xname, xdesc, content, xcode
        from gookhwe_stuffs.live_list
        where date0="{date0}"
        """
    )
    for temp in cursor.fetchall():
        content = temp[3]
        active = "True" if content else "False"
        cleaned_xsubj = re.sub(r'\[\d{1,2}:\d{2}\]', '', temp[0]).strip()
        objs_list.append({'xsubj':cleaned_xsubj, 'xname': temp[1], 'xdesc': temp[2], 'active':active, 'xcode': temp[4]})
    db.close()
    return jsonify(objs_list)

# 속기록 내용 업데이트를 위한 API
@app.route('/donga/gookhwe/<date0>/<xcode0>/article', methods=['GET'])
def article_request(xcode0, date0):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        f"""
        select content, xdesc
        from gookhwe_stuffs.live_list
        where xcode='{xcode0}' and date0="{date0}"
        """
    )
    result = cursor.fetchone()
    content = result[0]
    xdesc = result[1]
    cursor.close()

    if content is None:
        response = {
            'status': 'error',
            'article': '데이터 없음 (개의 전이거나 수집 가능 대상 아님)',
            'xdesc' : xdesc
        }
    else:
        if content is None:
            response = {
                'status': 'error',
                'article': '데이터 없음 (개의 전이거나 수집 가능 대상 아님)',
                'xdesc' : xdesc
            }
        else:
            blob_scrol = codecs.decode(content, 'utf-8')
            article = blob_scrol.replace('\n', '<BR>')
            response = {
                'status': 'success',
                'article': article,
                'xdesc' : xdesc
            }
    return jsonify(response)

if __name__ == "__main__":
    port = '443'
    host = '0.0.0.0'
    app.run(host=host, port=port, ssl_context='adhoc', debug=True)
