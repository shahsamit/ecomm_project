from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import dbfunctions,moreproducts
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("instance/todo.db")
cur = con.cursor()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Cart(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(500), nullable=True)
    name = db.Column(db.String(200), nullable=True)
    price= db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    total = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
            return f"{self.sno} - {self.name}"

#@app.route('/', methods=['GET', 'POST'])
#def hello_world():
 #   if request.method=='POST':
  #      title = request.form['title']
   #     desc = request.form['desc']
    #    todo = Todo(title=title, desc=desc)
     #  db.session.commit()
        
    #allTodo = Todo.query.all()
    #return render_template('index2.html', allTodo=allTodo)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        image = request.form['img']
        name = request.form['name']
        price = request.form['price']
        quantity= 1
        total= price*quantity
        todo = Cart(image=image,name=name,price=price,quantity=quantity,total=total)
        db.session.add(todo)
        db.session.commit()
    if not session.get("name"):
        msg='You are not logged in'
    else:
         msg='Welcome back, '+ session.get("name")
    return render_template('homepage.html',msg=msg)

#@app.route('/', methods=['GET', 'POST'])
#def hello_world():
#        if request.method=='POST':
 #           title = request.form['title']
  #          desc = request.form['desc']
   #         todo = Todo(title=title, desc=desc)
    #        db.session.commit()
     #   return render_template('homepage.html')



@app.route('/cart', methods=['GET', 'POST'])
def hello_world2():
        totalcart=dbfunctions.getTotal()
        allCart = Cart.query.all()
        return render_template('cart_page.html', allCart=allCart,totalcart=totalcart)

@app.route('/products', methods=['GET', 'POST'])
def hello_world3():
    if request.method=='POST':
        image = request.form['img']
        name = request.form['name']
        price = request.form['price']
        quantity= 1
        total= price*quantity
        todo = Cart(image=image,name=name,price=price,quantity=quantity,total=total)
        db.session.add(todo)
        db.session.commit()
    allproducts=moreproducts.getproducts()
    return render_template('category.html', allproducts=allproducts)

@app.route('/login', methods=['POST'])
def login_fn():
    if request.method=='POST':
        name = request.form['LoginForm-name']
        password = request.form['LoginForm-pass']
        if(dbfunctions.validateuser(name,password)):
             session["name"] = name
        return redirect("/")
        
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
        return render_template('checkout_page.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Cart.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/cart")

if __name__ == "__main__":
    app.run(debug=True, port=8000)