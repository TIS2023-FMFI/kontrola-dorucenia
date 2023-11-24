import sqlite3

def verify_user(mail, password):
    
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    select = """SELECT * FROM user
            WHERE email='{m}'
            AND password='{p}'""".format(m = mail, p = password)
    cursor.execute(select)
    user = cursor.fetchall();
    cursor.close()
    connection.close()

    return user
