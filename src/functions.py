import sqlite3
from flask_bcrypt import Bcrypt


def verify_user(mail, password):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select = """SELECT * FROM user
                        WHERE email=?"""
        cursor.execute(select, (mail,))
        fetch_user = cursor.fetchone()
        cursor.close()
        connection.close()
        return fetch_user if fetch_user and Bcrypt().check_password_hash(fetch_user[4], password) else None
