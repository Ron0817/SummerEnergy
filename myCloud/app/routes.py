import os
from flask import render_template, url_for, request, redirect, flash, session
from markupsafe import escape
from app import app
from app.user import User, total_users
from app.__init__ import memcache
from app.config import *
from werkzeug.utils import secure_filename
import base64

import mysql.connector
import threading
import time


app.config['MYSQL_CONFIG'] = mysql_config
app.config['USERS_FOLDER'] = USERS_FOLDER
app.config['DISPLAY_FOLDER'] = DISPLAY_FOLDER

# Default user
# current_user = User(fname='Please log in', email="default@gmail.com", password='default')
# total_users.update({current_user.email: current_user})

# Default posts
posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

# Index page
@app.route('/')
@app.route('/index')
def index():    
    if app.debug == True:
        if 'test@test.com' not in total_users:
            total_users.update({'test@test.com': User('Test', 'User', 'test', '123', 'test@test.com')})
            try:
                os.mkdir(os.path.join(app.config['USERS_FOLDER'], str(total_users['test@test.com'].id)))
            except OSError as error:
                print(error)
    if 'email' in session:
        current_user = total_users[session['email']]
        if app.debug == True:
            print('TOTAL USER LIST: {}'.format(total_users))
        return render_template('index.html', title='Home', user=current_user, posts=posts)
    else:
        return render_template('index.html', title='Home', posts=posts)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Do the login
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password']
        if app.debug == True:
            print('User input login info: email: %s password: %s' % (email, password))
        
        # Log in
        if email in total_users:
            current_user = total_users.get(email)
            if current_user.login(email, password):
                session['email'] = email
                session.permanent = False
                return redirect(url_for('index'))
            else:
                flash('Wrong user email or password. Try again.')
                return render_template('login.html', title='Login')
        # Sign up
        else:
            flash('Please sign up first.')
            return render_template('signup.html', title='Sign up')
        
    # Show the login form
    else:
        return render_template('login.html', title='Login')
    
# Sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password']
        lname = request.form['lname']
        fname = request.form['fname']
        number = request.form['number']
        
        # Already signed up
        if email in total_users:
            flash('Email already signed up. Try log in.')
            return redirect(url_for('login'))
        # Sign up
        else:
            new_user = User(fname, lname, password, number, email)
            total_users.update({email: new_user})
            try:
                os.mkdir(os.path.join(app.config['USERS_FOLDER'], str(new_user.id)))
            except OSError as error:
                print(error) 
            if app.debug == True:
                print('User signed up successfully - email: %s password: %s' % (email, password))
            flash('Email signed up successfully. Now log in.')
            return render_template('signup.html', title='signup')
        
    # Show the Signup form
    else:
        return render_template('signup.html', title='signup')

# Log out page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'email' in session:
        session.pop('email')
    else:
        flash("You are logged out")
    return redirect(url_for('index'))

# Allowed extension validation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Key file validation and store
def key_file_store(key, request):
    if 'image' not in request.files:
        flash('Please select a file')
    file = request.files['image']
    
    if file.filename == '':
        flash('No selected file')
    elif not allowed_file(file.filename):
        flash('Allowed file type are %s' % ALLOWED_EXTENSIONS)
    elif file:
        filename = secure_filename(file.filename)
        filename = key + '.' + filename
        file_binary = base64.b64encode(file.read())
        file_binary = file_binary.decode('utf-8') # remove b''
        file.save(os.path.join(app.config['USERS_FOLDER'], str(total_users[session['email']].id) ,filename))
        
        flash('File upload succeeded')
        return file_binary
    return None
        
@app.route('/mycontent', methods=['GET', 'POST'])
def mycontent():
    # Check if login
    if 'email' in session:            
        return render_template('mycontent.html')
    else:
        flash("Please login first")
        return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Check if login
    if 'email' in session:
        current_user = total_users[session['email']]
        # Upload
        if request.method == 'POST':
            # Check if key in form
            if request.form['upload'] == '':
                flash('Please input a key')
                return redirect(request.url)
            key = request.form['upload']
            # Check if key exists - change to rds later
            for root, dirs, files in os.walk(os.path.join(app.config['USERS_FOLDER'], str(current_user.id))):
                for file in files:
                    if key == file.split('.')[0]:
                        # User popup confirmation
                        os.remove(os.path.join(root, file))
                        flash("Key exist, file replaced")

            if app.debug == True:
                print('User input upload key %s' % key)
                print("user id is: " + str(total_users[session['email']].id))
                print("user email is: " + session['email'])

            # Check if file is valid and store it
            file_binary = key_file_store(key, request)
            
            # Update memcache
            memcache.put(key, file_binary)

        return redirect(url_for('mycontent'))     
    
            # ################# Update RD
    else:
        flash("Please login first")
        return redirect(url_for('login'))
    
@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    binary_flag = 0
    # Check if login
    if 'email' in session:
        # Retrieve
        key =  request.form['retrieve']
        current_user = total_users[session['email']]

        # Try memcache
        if key in memcache.itself():
            binary_flag = 1
            return render_template('display.html', file_path=memcache.get(key), key=key, binary_flag=binary_flag)

        # Else go to local storage
        for root, dirs, files in os.walk(os.path.join(app.config['USERS_FOLDER'], str(current_user.id))):
            for file in files:
                if key == file.split('.')[0]:
                    file_path = os.path.join(app.config['DISPLAY_FOLDER'], str(current_user.id), file)
                    
                    if app.debug == True:
                        print('User input retrieve key %s' % key)
                        print('User File Path: ' + file_path)
                    return render_template('display.html', file_path=file_path, key=key, binary_flag=binary_flag)

        flash('No file associated with the key was found')
        return redirect(url_for('mycontent'))
        # ################# Update RD
    else:
        flash("Please login first")
        return redirect(url_for('login')) 

# MyCloud Configuration
@app.route('/mycloud-config', methods=['GET', 'POST'])
def mycloud_config():
    # Check if login
    if 'email' in session:
        return render_template('mycloud-performance.html',keys=list(memcache.keys()))
    else:
        flash('Please login first')
        return redirect(url_for('login'))

# Memcache Configuration
@app.route('/memcache-config', methods=['GET', 'POST'])
def memcache_config():
    capacity = request.form['capacity']
    policy = request.form['policy']

    # Insert query
    query = '''INSERT INTO `memcache`.`config` (`id`, `policy`, `capacity`) VALUES (1, %s, %s)
        ON DUPLICATE KEY UPDATE `policy` = %s, `capacity` = %s'''
    cnx = mysql.connector.connect(**app.config['MYSQL_CONFIG'])
    cursor = cnx.cursor()
    cursor.execute(query, (policy, capacity, policy, capacity))
    cnx.commit()
    cnx.close()    

    # Memcache reconfiged
    memcache.refresh_configuration()
    flash("Memcache configured - Capacity: %s MB, Policy: %s " % (capacity, policy))

    if app.debug == True:
        print("Memcache reconfigured - new policy: %s, new capacity: %s" % (memcache.replacement_policy, memcache.capacity))
    return redirect(url_for('mycloud_config'))

# SQL query handler
# def insert_query_handler(queries, params):
#     cnx = mysql.connector.connect(**app.config['MYSQL_CONFIG'])
#     cursor = cnx.cursor()
#     for query in queries:
#         cursor.execute(query)
#     cnx.close()
#     if app.debug == True:
#         print("SQL Query executed")

# Memcache Configuration
@app.route('/memcache-statistics', methods=['GET', 'POST'])
def memcache_statistics():
    return "reached here"
    capacity = request.form['capacity']
    policy = request.form['policy']

    # Insert query
    query = '''INSERT INTO `memcache`.`config` (`id`, `policy`, `capacity`) VALUES (1, %s, %s)
        ON DUPLICATE KEY UPDATE `policy` = %s, `capacity` = %s'''
    cnx = mysql.connector.connect(**app.config['MYSQL_CONFIG'])
    cursor = cnx.cursor()
    cursor.execute(query, (policy, capacity, policy, capacity))
    cnx.commit()
    cnx.close()    

    # Memcache reconfiged
    memcache.refresh_configuration()
    flash("Memcache configured - Capacity: %s MB, Policy: %s " % (capacity, policy))

    if app.debug == True:
        print("Memcache reconfigured - new policy: %s, new capacity: %s" % (memcache.replacement_policy, memcache.capacity))
    return redirect(url_for('mycloud_config'))

