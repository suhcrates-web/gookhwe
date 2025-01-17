from database import db, cursor
import mysql.connector
from datetime import date

def live_list_start():
    config = {
        'user': 'root',
        'password': 'donga123123!',
        'host': 'localhost',
        # 'database':'shit',
        'port': '3306'
    }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()

        #초기. 테이블 지우고 만들어야 할 때
    cursor.execute(
        """
        drop table if exists gookhwe_stuffs.live_list
        """

    )
    cursor.execute(
        """
        create table if not exists gookhwe_stuffs.live_list(
        date0 date,
        key0 varchar(20) primary key,
        xcode varchar(20),
        xstat varchar(1),
        xname varchar(100),
        xdesc varchar(20),
        xcgcd varchar(20),
        xsubj varchar(100),
        xthmb varchar(100),
        wss varchar(100),
        content longblob,
        summary blob,
        chair json,
        )
        """
    )

    # cursor.execute(
    #     f"""
    #     delete from gookhwe_stuffs.live_list where date0 != '{date.today()}'
    #     """
    # )