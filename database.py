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
            sql = f"INSERT INTO users (userid, username, discriminator) VALUES ({int(userid)}, {str(username)}, {int(discrim)});"
            #sql = "CREATE TABLE UserTests (test1 INT);"
            #vals = (userid, username, discrim)
            c.execute(sql)
            conn.commit()
            c.close()
        else:
            print('Connection failed.')
    except Error as e:
        return e
