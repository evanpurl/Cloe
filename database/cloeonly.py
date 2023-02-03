from mysql.connector import MySQLConnection, Error
from database.python_mysql_dbconfig import read_db_config
import random

async def getgreeting(greeting):
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
                return None
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

async def getily(ily):
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


async def getcompliment(compliment):
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

async def setauthuser(user):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"INSERT INTO authorized (authusers) VALUES (%(authusers)s);"
            user_data = {
                'authusers': user,
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


async def getauthuser(user):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"SELECT authusers from authorized where authusers=%(authusers)s;"
            user_data = {
                'authusers': user,
            }
            c.execute(sql, user_data)
            role = c.fetchone()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
            if role:
                return True
            else:
                return False
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e