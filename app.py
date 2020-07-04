import os
import psycopg2
import requests
import json
from functools import wraps
from flask import abort, jsonify
from functools import wraps
from flask import Flask,g,flash, render_template, request, session, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request  
from sqlalchemy import func

from models import * 



def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:            
            return redirect(url_for('index'))
    return wrap


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  


app.secret_key =  os.getenv("SECRET_KEY")
db.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#------------------------------------------------Render Routes----------------------------------------------------------------
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route("/")
def index():
    try: 
        logged = session['logged_in']
    except:
        logged = False
        session['username'] = None

    return render_template("index.html" , logged = logged , session_username = session['username'])

@app.route("/signup_page")
def signup_page():
    return render_template("signup.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/signup", methods=["POST"]) 
def signup():
    email= request.form.get("sign_email")
    password = request.form.get("sign_pswd")
    username = request.form.get("sign_username")   
    
    if User.query.filter_by(email=email).count()==0:
        user=User(email=email, password=password)
        user.phone = request.form.get("sign_num")
        user.address =  request.form.get("sign_address") 
        user.username =  username  
        db.session.add(user)
        db.session.commit()

        flash('Successfully signed up.')
        return redirect(url_for('login_page'))            
    else: 
        flash('Error! Email is registered.')
        return redirect(url_for('index'))       

@app.route("/login", methods=["POST"]) 
def login():
    email = request.form.get("log_email")
    password =  request.form.get("log_pswd")
    user= User.query.filter(and_( User.email == email, User.password == password)).first()
    if  user == None: 
        flash('Error! Email and Password do not match.')
        return redirect(url_for('index'))  
    session['logged_in']=True
    session['username'] = user.username
    session['email'] = email
    return redirect(url_for('profile'))

@app.route("/profile")
@login_required
def profile():
    user= User.query.filter( User.username ==  session['username']).first()
    return render_template("profile.html", User = user )

@app.route("/logout" , methods=["GET", "POST"])
@login_required
def logout():
    session.pop('logged_in', None)
    session.clear()    
    return redirect(url_for('index'))

@app.route("/delete_account" , methods=["POST"])
@login_required
def delete_account():
    user = User.query.filter_by(email=session['email']).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('logout'))




