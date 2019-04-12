#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, flash, url_for
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        print((form_username))
        print([form_username])
        cur = mysql.connection.cursor()
        row = cur.execute("SELECT * FROM admin WHERE username = %s;", [form_username])
        if row > 0:
            cur.execute("SELECT password FROM admin WHERE username = %s;", [form_username])
            admin_password = cur.fetchone()
            if admin_password[0] == form_password:
                flash('You were successfully logged in')
                return redirect('/users')
            else:
                flash('Invalid Credentials')
                #return redirect(url_for('index'))
        else:
            flash('Invalid Credentials')
            #return redirect(url_for('index'))
        cur.close()
    return render_template('login.html')


@app.route('/add_user_profile', methods=['GET', 'POST']) #add route to add_user_profile page / add methods
def add_user_profile():
    if request.method == 'POST':
        #Fetch form data
        user_name = request.form['user_name']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        home_address = request.form['home_address']
        print((user_name))
        cur = mysql.connection.cursor()
        sql = "INSERT INTO users (user_name, mobile_number, email, home_address) VALUES (%s, %s, %s, %s);"
        data = (user_name, mobile_number, email, home_address,)
        cur.execute(sql, data) #insert new inputs to database
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
    return render_template('new_profile.html', userDetails=userDetails)


@app.route('/users', methods=['POST'])
def users(): #define new_profile page
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users;")
    if resultValue > 0: #check if there are rows (=content) i.e. not empty table
        userDetails = cur.fetchall() #returns all rows
    if request.method == 'POST':
        if request.form['edit_button']:
            return redirect('/edit_profile')
        elif request.form['delete_button']:
            cur.execute("DELETE FROM users WHERE id = %s;", (id))
            mysql.connection.commit()
            flash('Profile deleted successfully')
        elif request.form['add_button']:
            return redirect('/add_user_profile')
    cur.close()
    return render_template('users.html', userDetails=userDetails) #render a template to display all user details


@app.route('/edit_user_profile/<int:id>', methods=['GET', 'POST']) #add route to add_user_profile page / add methods
def edit_user_profile(id):
    if request.method == 'POST':
        #Fetch form data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s;", (id))
        userDetails = cur.fetchone()
        user_name = request.form['user_name']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        home_address = request.form['home_address']
        sql = "REPLACE INTO users (user_name, mobile_number, email, home_address) VALUES (%s, %s, %s, %s) where id = %s;"
        data = (user_name, mobile_number, email, home_address, id)
        cur.execute(sql, data) #insert new inputs to database
        mysql.connection.commit() #commit changes to database
        flash('Profile edited successfully')
        return redirect('/users')
        cur.close()
    return render_template('edit_user_profile.html') #render a template to display the form



@app.route('/delete_user_profile/<int:id>')
def delete_user(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users where id = %s;", (id,))
        mysql.connection.commit()
        flash('Profile deleted successfully')
        return redirect('/users')
    cur.close()



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True) #debug mode to avoid restarting the server for changes
