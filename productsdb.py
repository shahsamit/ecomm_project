import json
import sqlite3

con = sqlite3.connect("instance/todo.db")
cur = con.cursor()
#cur.execute('Create Table if not exists productsinfo (prod_img Text, prod_name Text, prod_price Integer)')

records = [('./static/img/products/02.jpg','Tropical Shirt Dress',100),
('./static/img/products/03.jpg','Shoulder Embroidered Bodysuit',110),
('./static/img/products/04.jpg','Checked Polo Collar T-shirt',150),
('./static/img/products/05.jpg','Crochet Detail Lightweight Top',100),
('./static/img/products/06.jpg','Girls Floral Print Jumpsuit',90),
('./static/img/products/07.jpg','Girls Striped Fit and Flare Dress',100),
('./static/img/products/08.jpg','Juventus Henley Neck Jersey',100),
('./static/img/products/09.jpg','Printed Dugaree with T-Shirt',100),
('./static/img/products/10.jpg','Printed Polo Collar T-shirt',100)
]

cur.executemany('INSERT INTO ProductsInfo VALUES(?,?,?);',records);


con.commit() 
for row in cur.execute('SELECT * FROM ProductsInfo'):
    print(row)
con.close()