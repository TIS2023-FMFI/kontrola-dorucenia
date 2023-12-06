import sqlite3

def verify_user(mail, password):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    select = """SELECT * FROM user
            WHERE email='{m}'
            AND password='{p}'""".format(m = mail, p = password)
    cursor.execute(select)
    user = cursor.fetchall()
    cursor.close()
    connection.close()
    return user

def change_password(new_password, email):
    connection = sqlite3.connect('database.db')
    update = """UPDATE user 
        SET password='{p}'
        WHERE email='{e}'""".format(p = new_password, e = email)
    connection.execute(update)
    connection.commit()
    connection.close()
    return 
    
def add_user(name, email, password, admin):
    connection = sqlite3.connect('database.db')
    insert = """INSERT INTO user 
                (admin, name, email, password) VALUES
                ('{a}', '{n}', '{e}', '{p}')""".format(a = admin, n = name, e = email, p = password)
    connection.execute(insert)
    connection.commit()
    connection.close()
    return 

def get_users():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    connection.close()
    return users

def delete_user(users):
    connection = sqlite3.connect('database.db')
    for user_id in users:
        delete = "DELETE FROM user WHERE id='{id}'".format(id = user_id)
        connection.execute(delete)
    connection.commit()
    connection.close()
    return 
    
