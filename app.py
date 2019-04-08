#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import yaml
import os


app = Flask(__name__) #instantiate object to run flask application

db = yaml.full_load(open('db.yaml')) #database accesses yaml file of parameters
#Configure parameters to connect to database
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app) #instantiate object to connect to MySQL

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        cur = mysql.connection.cursor()
        row = cur.execute("SELECT * FROM admin WHERE username = %s;", [form_username])
        if row > 0:
            cur.execute("SELECT password FROM admin WHERE username = %s;", [form_username])
            admin_password = cur.fetchone()
            if admin_password[0] == form_password:
                return redirect('/users')
            else:
                flash('Invalid Credentials')
                print('line 35')
                #return index()
        else:
            flash('Invalid Credentials')
            print('line 39')
            #return index()
        cur.close()
    return render_template('index.html')


@app.route('/add_user_profile', methods=['GET', 'POST']) #add route to add_user_profile page / add methods
def add_user_profile(): #define index page
    if request.method == 'POST':
        #Fetch form data
        userDetails = request.form
        user_name = userDetails['user_name']
        mobile_number = userDetails['mobile_number']
        email = userDetails['email']
        home_address = userDetails['home_address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(user_name, mobile_number, email, home_address) VALUES(%s, %s, %s, %s)", (user_name, mobile_number, email, home_address)) #insert new inputs to database
        mysql.connection.commit() #commit changes to database
        cur.close()
        return redirect('/new_profile') #redirect to new_profile page
    return render_template('add_user_profile.html') #render a template to display the form


@app.route('/new_profile') #add route to new_profile page
def new_profile(): #define new_profile page
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users order by id desc limit 1;") #returns latest entry
    if resultValue > 0: #check if there are rows (=content) i.e. not empty table
        userDetails = cur.fetchall() #returns all rows (in this case the only one that we selected3)
    cur.close()
    return render_template('new_profile.html', userDetails=userDetails) #render a template to display new user details


@app.route('/users') #add route to new_profile page
def users(): #define new_profile page
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users;")
    if resultValue > 0: #check if there are rows (=content) i.e. not empty table
        userDetails = cur.fetchall() #returns all rows
    cur.close()
    return render_template('users.html', userDetails=userDetails) #render a template to display all user details



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True) #debug mode to avoid restarting the server for changes
