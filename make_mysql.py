from database import cursor, db

cursor.execute(
    f"""
    CREATE database if not exists gookhwe_stuffs;
    """
)
cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS gookhwe_stuffs.temp_checker(
        ind0 varchar(30) primary key,
        xcode varchar(20),
        xname varchar(20),
        xdesc varchar(20),
        xcgcd varchar(20)
        );
        """
    )
cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS gookhwe_stuffs.live_list(
        date0 datetime,
        key0 varchar(20) primary key,
        xcode varchar(20),
        xstat varchar(1),
        xname varchar(20),
        xdesc varchar(20),
        xcgcd varchar(20),
        xsubj varchar(50),
        content longblob,
        summary blob
        );
        """
    )
# cursor.execute(
#         f"""
#         CREATE TABLE IF NOT EXISTS gookhwe_stuffs.temp_checker(
#         ind0 varchar(30) primary key,
#         xcode varchar(20),
#         xname varchar(20),
#         xdesc varchar(20),
#         xcgcd varchar(20),
#         xsubj varchar(50),
#         content blob
#         );
#         """
#     )


#

#
# cursor.execute(
#     """
#     insert into gookhwe_stuffs.council values('test',NULL,NULL,NULL )
#     """
# )
db.commit()
