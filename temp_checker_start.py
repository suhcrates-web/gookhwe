from database import db, cursor
from datetime import datetime


def temp_checker_start():
    cursor.execute(
        """
        select xcode, xname, xdesc, xcgcd from gookhwe_stuffs.live_list
        """
    )

    list0 = []
    today0 = datetime.today().strftime("%Y%m")

    for xcode, xname, open0, xcgcd in cursor.fetchall():


        cursor.execute(

            f"""insert into gookhwe_stuffs.temp_checker values("{today0}_{xcode}", "{xcode}","{xname}", "{open0}", "{xcgcd}")"""
        )
    db.commit()

