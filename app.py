from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import dbfunctions,moreproducts,MLFunctions
from flask_session import Session
import io
from flask import Response
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px

from io import BytesIO
import random

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

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

class products(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    prod_img = db.Column(db.String(200), nullable=False)
    prod_name = db.Column(db.String(500), nullable=False)
    prod_price = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
            return f"{self.sno} - {self.prd_name}"

@app.route('/print-plot')
def plot_png2():
    return render_template('dashboard.html')

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig, ax = plt.subplots(figsize = (6,4))
    top10=MLFunctions.getdata()
    x = top10.index
    y = top10.values
    ax.bar(x, y)
    return fig

@app.route('/chart')
def bar_with_plotly():
   
    top10=MLFunctions.getdata()
    fig = px.bar(top10, x=top10.index, y=top10.values,  barmode='group')
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    top10=MLFunctions.getdata()
    freq1=MLFunctions.frequentproducts()
    assoc1=MLFunctions.getassoc_rules()
    freq=list(freq1.itemsets)
    assoc=set(assoc1.consequents)
    print(freq)
    print(assoc)
    return render_template('dashboard.html', graphJSON=graphJSON,top10=top10,freq=freq,assoc=assoc)
 

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
    #prdinfo=dbfunctions.getprd_info()
    #prdinfo=products.query.all()
    prdinfo=dbfunctions.getprd_info()
    tcount=dbfunctions.getCount()
    totalcart=dbfunctions.getTotal()
    allCart = Cart.query.all()
    return render_template('homepage.html',prdinfo=prdinfo,msg=msg,tcount=tcount, allCart=allCart,totalcart=totalcart)

@app.route('/cart', methods=['GET', 'POST'])
def hello_world2():
        totalcart=dbfunctions.getTotal()
        tcount=dbfunctions.getCount()
        allCart = Cart.query.all()
        return render_template('cart_page.html', allCart=allCart,totalcart=totalcart,tcount=tcount)

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
    tcount=dbfunctions.getCount()
    totalcart=dbfunctions.getTotal()
    allCart = Cart.query.all()
    return render_template('category.html', allproducts=allproducts,tcount=tcount, allCart=allCart,totalcart=totalcart)

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

@app.route('/deletehomepage/<int:sno>')
def deletehomepageproduct(sno):
    todo = Cart.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/add/<int:sno>',methods=['GET', 'POST'])
def add(sno):
    dbfunctions.addproduct(sno)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)