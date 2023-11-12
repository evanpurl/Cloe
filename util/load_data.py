import discord

from util.databasefunctions import create_pool, getall, createserver
from util.sqlitefunctions import create_db, createuniqueindex, create_table


async def loadallservers(bot, serverlist):
    servers = []
    for a in serverlist:
        servers.append(a.id)
    await loaddata(bot, servers)


async def loaddata(bot, guildlist):
    """
    Function that loads sqlite data.
    :param guildlist:
    :param bot:
    :return:
    """
    try:
        pool = await create_pool()

        data = await getall(pool, f"SELECT serverid FROM {bot.user.name}")

        missing = set(guildlist).difference(data)

        if len(missing) > 0:
            pool = await create_pool()
            for a in missing:
                guild = await bot.fetch_guild(a)
                print(f"Creating data for {guild.name}")
                await createserver(pool, f"""INSERT IGNORE INTO {bot.user.name} (serverid) VALUES ({guild.id});""")
                print(f"Data confirmed for guild {guild.name}")

        print("Data confirmed")

        #  SE Specific Section
        guild = await bot.fetch_guild(955962668756385792)
        tabledata = """CREATE TABLE IF NOT EXISTS SE ( userid integer NOT NULL, roleid integer);"""
        conn = await create_db(f"storage/{guild.id}/SE.db")
        await create_table(conn, tabledata)
        await createuniqueindex(conn, f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_userid ON SE (userid) """)
        print("Loaded SE Data.")
        #
    except Exception as e:
        print(f"load data function, ({e})")
