from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import random


########################################################
################### MySQL Defines ######################
###################   Testing     ######################
########################################################


def getgreeting(greeting):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            # print('Processing Greeting.')
            c = conn.cursor()
            sql = f"SELECT responses from greetings where greeting=%(greeting)s;"
            user_data = {
                'greeting': greeting,
            }
            c.execute(sql, user_data)
            response = c.fetchone()
            if not response:
                # sql = f"INSERT INTO greetings (greeting, responses) VALUES (%(greeting)s, %(responses)s);"
                # user_data = {
                #     'greeting': greeting,
                #     'responses': "None",
                # }
                # c.execute(sql, user_data)
                # conn.commit()
                return None
            response = list(response)
            response = response[0].split(", ")
            choice = random.choice(response)
            c.close()
            conn.close()
            return choice
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def setmodrole(role, server):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"UPDATE servers SET editrole = %(editrole)s WHERE serverid = %(server)s;"
            user_data = {
                'editrole': role,
                'server': server,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def setsupprole(role, server):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"UPDATE servers SET supporterrole = %(supporterrole)s WHERE serverid = %(server)s;"
            user_data = {
                'supporterrole': role,
                'server': server,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def getmodrole(server):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"SELECT editrole from servers where serverid=%(serverid)s;"
            user_data = {
                'serverid': server,
            }
            c.execute(sql, user_data)
            role = c.fetchone()
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
            return role
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def getsupprole(server):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"SELECT supporterrole from servers where serverid=%(serverid)s;"
            user_data = {
                'serverid': server,
            }
            c.execute(sql, user_data)
            role = c.fetchone()
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
            return role
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def createserver(server):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"INSERT INTO servers (serverid) VALUES (%(serverid)s);"
            user_data = {
                'serverid': server,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def deleteserver(server):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"DELETE FROM servers WHERE serverid = (%(serverid)s);"
            user_data = {
                'serverid': server,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


def getily(ily):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            # print('Processing Affirmation.')
            c = conn.cursor()
            sql = f"SELECT responses from affirmations where affirmation=%(affirmation)s;"
            user_data = {
                'affirmation': ily,
            }
            c.execute(sql, user_data)
            response = c.fetchone()
            if not response:
                return None
            response = list(response)
            response = response[0].split(", ")
            choice = random.choice(response)
            c.close()
            conn.close()
            return choice
        else:
            return 'Connection to database failed.'
    except Exception as e:
        print(e)
        return e


def getcompliment(compliment):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            # print('Processing Compliment.')
            c = conn.cursor()
            sql = f"SELECT responses from compliments where compliment=%(compliment)s;"
            user_data = {
                'compliment': compliment,
            }
            c.execute(sql, user_data)
            response = c.fetchone()
            if not response:
                return None
            response = list(response)
            response = response[0].split(", ")
            choice = random.choice(response)
            c.close()
            conn.close()
            return choice
        else:
            return 'Connection to database failed.'
    except Exception as e:
        print(e)
        return e
