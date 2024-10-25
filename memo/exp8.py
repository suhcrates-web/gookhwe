import binascii, codecs
from database import cursor, db


cursor.execute(
    """
    select content from gookhwe_stuffs.council where council='test'
    """
)
a = cursor.fetchall()[0][0]
temp = codecs.decode(a, 'utf-8')
print(temp.strip().split('\n'))

