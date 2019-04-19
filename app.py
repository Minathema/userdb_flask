#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL
import yaml
import os
import re


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
    condition = False
    if request.method == 'POST':
        while condition == False :
        #Fetch form data
            user_name = request.form['user_name']
            telephone = (request.form['telephone']).replace(" ", "") #remove spaces from 'telephone'
            mobile_number = (request.form['mobile_number']).replace(" ", "") #remove spaces from 'mobile_number'
            email = ((request.form['email']).replace(" ", "")).lower() #remove spaces from 'email' and make lowercase
            home_address = request.form['home_address']
            print('NNNNNNNNNNNNN: line60', user_name, telephone[:2], mobile_number, email, home_address)

            #check if 'user_name' is empty or contains numbers (regex)
            if not user_name or bool(re.search(r'\d', user_name)) == True:
                flash('Please add a valid name')
                print('NNNNNNNNNNNNN: line64')
                return redirect('/add_user_profile')

            #check if both 'telephone' and 'mobile_number' are empty
            elif not telephone and not mobile_number:
                flash('Please add at least one contact number')
                print('NNNNNNNNNNNNN: line68', mobile_number)
                return redirect('/add_user_profile')

            #check if 'telephone' is not empty
            elif telephone == True:
                #check if 'telephone' contains not only numbers or does not consist of 10 characters or does not start with '21'
                if telephone.isdigit() == False or len(telephone) != 10 or telephone[:2] != '21':
                    flash('Please add a valid telephone number')
                    print('NNNNNNNNNNNNN: line73', telephone)
                    return redirect('/add_user_profile')

            #check if 'mobile_number' is not empty
            elif mobile_number == True:
                #check if 'telephone' contains not only numbers or does not consist of 10 characters or does not start with '69'
                if mobile_number.isdigit() == False or len(mobile_number) != 10 or mobile_number[:2] != '69':
                    flash('Please add a valid mobile number')
                    print('NNNNNNNNNNNNN: line78', mobile_number)
                    return redirect('/add_user_profile')

            #check if 'email' is valid (regex)
            elif bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)) == None:
                flash('Please add a valid email')
                print('NNNNNNNNNNNNN: line83', email)
                return redirect('/add_user_profile')

            #check if 'home_address' consists of numbers only
            elif home_address.isdigit() == True:
                flash('Please add a valid home address')
                print('NNNNNNNNNNNNN: line88', home_address)
                return redirect('/add_user_profile')

            #stops loop if all inputs are valid
            else:
                condition = True


        cur = mysql.connection.cursor()
        sql = "INSERT INTO users (user_name, telephone, mobile_number, email, home_address) VALUES (%s, %s, %s, %s, %s);"
        data = (user_name, telephone, mobile_number, email, home_address)
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


@app.route('/users', methods=['GET'])
def users(): #define new_profile page
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users;")
    if resultValue > 0: #check if there are rows (=content) i.e. not empty table
        userDetails = cur.fetchall() #returns all rows

    cur.close()
    return render_template('users.html', userDetails=userDetails) #render a template to display all user details


@app.route('/edit_user_profile/<int:id>', methods=['GET', 'POST']) #add route to add_user_profile page / add methods
def edit_user_profile(id):

    #Fetch form data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s;", [id])
    userDetails = cur.fetchone()

    if request.method == 'POST':
        user_name = request.form['user_name']
        telephone = request.form['telephone']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        home_address = request.form['home_address']


        sql = "REPLACE INTO users SET id = %s, user_name = %s, telephone = %s, mobile_number = %s, email = %s, home_address = %s;"
        data = (id, user_name, telephone, mobile_number, email, home_address)
        cur.execute(sql, data)

        mysql.connection.commit() #commit changes to database
        flash('Profile edited successfully')
        return redirect('/users')
    cur.close()
    return render_template('edit_user_profile.html', userDetails=userDetails) #render a template to display the form


@app.route('/delete_user_profile/<int:id>', methods=['POST'])
def delete_user_profile(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id =%s;", [id])
        mysql.connection.commit()
        flash('Profile deleted successfully')
        return redirect('/users')
        cur.close()



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True) #debug mode to avoid restarting the server for changes
