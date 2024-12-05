import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", password="", database="test")

def connectioned():
    if connection.is_connected():
        print("Udalo sie")
    else:
        print("Cos nie pyklo")

    mycur=connection.cursor()
    mycur.execute("SELECT * FROM test")

    result=mycur.fetchall()

    for row in result:
        print (row)
        
    connection.close()

connectioned()
