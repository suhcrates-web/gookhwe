# from database import cursor, db
import mysql.connector
config = {
        'user': 'root',
        'password': 'donga123123!',
        'host': 'localhost',
        'database':'gookhwe_stuffs',
        'port': '3306'
    }

db = mysql.connector.connect(**config)
cursor = db.cursor()
cursor.execute(
    """
    alter table gookhwe_stuffs.council modify column `content` mediumblob;
    """
)
db.commit()