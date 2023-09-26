import os.path
from sqlite3 import Error

from util.sqlitefunctions import create_db, create_table, createuniqueindex


async def loadallservers(serverlist):
    for a in serverlist:
        await loaddata(a.id)


async def loadserverdata(guildid):
    await loaddata(guildid)


async def loaddata(guildid):
    """
    Function that loads sqlite data.
    :type guildid: int
    :return:
    """
    if not os.path.exists(f"storage/{guildid}"):
        os.makedirs(f"storage/{guildid}", exist_ok=True)
    if not os.path.exists(f"storage/global"):
        os.makedirs(f"storage/global", exist_ok=True)
    try:
        tabledata = """CREATE TABLE IF NOT EXISTS config ( configname text NOT NULL, option integer);"""
        conn = await create_db(f"storage/{guildid}/configuration.db")
        await create_table(conn, tabledata)
        await createuniqueindex(conn, f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_config ON config (configname) """)
        # Will add more files as needed.
        print("Data confirmed!")
    except Error or Exception as e:
        print(f"load data function, guildid {guildid} ({e})")
