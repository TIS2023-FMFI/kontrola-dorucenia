import sqlite3
 
try:
   
    # Connect to DB and create a cursor
    connection = sqlite3.connect('sql.db')
    cursor = connection.cursor()
 
    # Write a query and execute it with cursor
    query = 'select sqlite_version();'
    cursor.execute(query)
 
    # Fetch and output result
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))
     
    # CREATE TABLE
    table = """CREATE TABLE IF NOT EXISTS STUDENT
                (NAME VARCHAR(255),
                CLASS VARCHAR(255));"""

    # Vykonanie príkazu
    cursor.execute(table)

    # Commit
    connection.commit()

    print("Table created successfully")

    # INSERT 
    cursor.execute('''INSERT INTO STUDENT VALUES ('Adam', '3A')''') 
    cursor.execute('''INSERT INTO STUDENT VALUES ('Tomas', '5B')''') 
    cursor.execute('''INSERT INTO STUDENT VALUES ('Jakub', '1C')''') 
      
    # SELECT a vypísanie hodnôt
    print("Data Inserted in the table: ") 
    data=cursor.execute('''SELECT * FROM STUDENT''') 
    for row in data: 
        print(row) 

    # Commit
    connection.commit() 
 
    # Close the cursor
    cursor.close()
 
# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure
finally:
   
    if connection:
        connection.close()
        print('SQLite Connection closed')
