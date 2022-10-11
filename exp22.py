import mysql.connector

config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        'port': '3306'
    }
db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute(
    """
    create table gookhwe_stuffs.test3(
    id varchar(3) primary key,
    state varchar(10),
    open0 varchar(10)
    )
    """
)