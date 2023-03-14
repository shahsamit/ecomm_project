import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("instance/todo.db")

cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT password FROM user where username ="johnd"'):
    passwd=row[0]

print(passwd)


    
# Be sure to close the connection
con.close()