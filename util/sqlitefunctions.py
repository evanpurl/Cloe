import sqlite3
from sqlite3 import Error


async def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error or Exception as e:
        print(f"create db: {e}")


async def create_table(conn, tabledata):
    """ create a table from the create_table_sql statement
    :param tabledata: Data to create in table
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(tabledata)
        c.close()

    except Error or Exception as e:
        print(f"create table: {e}")


async def insertconfig(conn, configlist):
    # config list should be a length of 2.
    try:
        datatoinsert = f""" REPLACE INTO config(configname, option) VALUES( ?, ?) """
        c = conn.cursor()
        c.execute(datatoinsert, (configlist[0], str(configlist[1])))
        conn.commit()
        c.close()
        conn.close()

    except Error or Exception as e:
        print(f"insert config: {e}")


async def createuniqueindex(conn, datatoinsert):
    try:
        c = conn.cursor()
        c.execute(datatoinsert)
        conn.commit()
        c.close()
        conn.close()
    except Error or Exception as e:
        print(f"createuniqueindex: {e}")


async def getconfig(conn, configoption):
    try:
        c = conn.cursor()
        c.execute(""" SELECT option FROM config WHERE configname=? """, [configoption])
        option = c.fetchone()
        if not option:
            return 0
        if len(option) == 0:
            return 0
        return option[0]
    except Error or Exception as e:
        print(f"get config: {e}")
        return []
