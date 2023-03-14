import sqlite3
# Create a SQL connection to our SQLite database
#con = sqlite3.connect("instance/todo.db", check_same_thread=False)

#cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
#for row in cur.execute('SELECT * FROM cart'):
#    print(row)
def getTotal():
    with sqlite3.connect("instance/todo.db") as con:
        name = "bob"
        cur = con.cursor()
        for row in cur.execute('SELECT SUM(total) FROM cart'):
            print(row[0])
            return(row[0])


    
# Be sure to close the connection
#con.close()