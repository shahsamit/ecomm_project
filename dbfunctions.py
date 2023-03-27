import sqlite3
#import pandas as pd
# Create a SQL connection to our SQLite database
#con = sqlite3.connect("instance/todo.db", check_same_thread=False)

#cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
#for row in cur.execute('SELECT * FROM cart'):
#    print(row)
def getTotal():
    with sqlite3.connect("instance/todo.db") as con:
        cur = con.cursor()
        for row in cur.execute('SELECT SUM(total) FROM cart'):
            return(row[0])
        
def getCount():
    with sqlite3.connect("instance/todo.db") as con:
        cur = con.cursor()
        for row in cur.execute('SELECT count(1) FROM cart'):
            return(row[0])

def validateuser(name,password):
    with sqlite3.connect("instance/todo.db") as con:
        cur = con.cursor()
        query='SELECT password FROM user where username ="'+name+'"'
        for row in cur.execute(query):
            print(row[0])
            passwd=row[0]
        if(passwd==password):
            print('-------------------------------login successful')
            return True
        print('-------------------------------login unsuccessful')
        return False
    
def getprd_info():
    with sqlite3.connect("instance/todo.db") as con:
        cur = con.cursor()
        prd_list=[]
        #prd_head=['prod_img','prod_name','prod_price']
        for row in cur.execute('SELECT * FROM productsinfo'):
            prd_list.append(row)
        #df=pd.DataFrame(prd_list)
        #df.columns = prd_head
        
        #return(df)
        return(prd_list)
        
def addproduct(sno):
    with sqlite3.connect("instance/todo.db") as con:
        cur = con.cursor()
        cur.execute('insert into Cart(image,name,price,quantity,total) SELECT prod_img , prod_name, prod_price,1,prod_price FROM productsinfo where sr_no='+str(sno))
        print('====================================================inserted into cart')
#con.close()


