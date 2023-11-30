import sqlite3
from flask_bcrypt import Bcrypt 


try:
   
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
     
    table_user = """CREATE TABLE IF NOT EXISTS user
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin BOOLEAN,
                name VARCHAR,
                email VARCHAR UNIQUE,
                password VARCHAR);"""

    table_request = """CREATE TABLE IF NOT EXISTS request
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES user(id),
                order_code VARCHAR(11),
                carrier_email VARCHAR,
                send_date DATE,
                send_time TIME,
                additional_message TEXT,
                response BOOLEAN);"""
    
    table_response = """CREATE TABLE IF NOT EXISTS response
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id REFERENCES request(id),
                type VARCHAR,
                delay BOOLEAN,
                root_cause VARCHAR,
                estimated_date DATE,
                estimated_time TIME,
                comment TEXT);"""


    hashed_password = Bcrypt().generate_password_hash('Admin Password')
    

    create_admin = """INSERT INTO user(admin, name, email, password)
                VALUES (true, ?, 'admin@example.com', ?);"""
    
    cursor.execute(table_user)

    cursor.execute(table_request)

    cursor.execute(table_response)
    
    cursor.execute(create_admin, ('Admin User', hashed_password))


    connection.commit()

    cursor.close()
 
except:
    
    connection.rollback()
 
finally:
    
    if connection:
        connection.close()
        
        



        
