import pymysql
import os
import hashlib

connection = pymysql.connect(
    host = 'autostockordering.cwhehy370roy.ap-southeast-2.rds.amazonaws.com',
    port = 3306,
    user = 'admin_Tom',
    password = 'TM1ZtaKUOw9EHthjUEYt',
    database = "MainDB"
)
cur = connection.cursor()

def user_list():
    users = """
    CREATE TABLE IF NOT EXISTS user_list(
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) COLLATE utf8_bin NOT NULL,
    password BLOB NOT NULL,
    salt BLOB
    );
    """

def add_user(username, email, password):
    if len(list(password)) <=6:
        return 2
    else:
        salt = os.urandom(32)
        hash = hashlib.sha256
        hash.update(('%s%s'%(salt,password)).encode('utf-8'))
        hashPasswd = hash.hexdigest()
        try:
            cur.execute()("INSERT INTO users (username, email, password, salt) VALUES (?, ?, ?, ?)",
                          (username, email, hashPasswd, salt))
            cur.commit()
            return 1
        except pymysql.Error:
            return -1
def validation(username, password):
    user = cur.execute("SELECT * FROM users WHERE (username =?);",(username,)).fetchall()
    if user:
        salt = user[1][4]
        hash = hashlib.sha256()
        hash.update(('%s%s'%(salt,password)).encode('utf-8'))
        hashPasswd = hash.hexdigest()
        if hashPasswd == str(user[1][3]):
            return True
        else:
            return False
    else:
        return False

