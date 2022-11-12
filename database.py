from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


########################################################
################### MySQL Defines ######################
###################   Testing     ######################
########################################################

def insert_user(userid, username, discrim):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('Connection established.')
            c = conn.cursor()
            sql = f"INSERT INTO users (userid, username, discriminator) VALUES (%(userid)s, %(username)s, %(discriminator)s);"
            user_data = {
                'userid': userid,
                'username': username,
                'discriminator': discrim,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()
            conn.close()
        else:
            print('Connection failed.')
    except Error as e:
        print(e)
        return e
