from flask import render_template, url_for, request, redirect
from markupsafe import escape
from app import app
from app.user import User, total_users

# Default user
current_user = User(fname='Please log in', email="default@gmail.com", password='default')
total_users.update({current_user.email: current_user})

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
        print('Now Current User on the Index Page is %s %s' % (current_user.fname, current_user.lname))
    return render_template('index.html', title='Home', user=current_user, posts=posts)

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
            global current_user
            current_user = total_users.get(email)
            if current_user.login(email, password):
                if app.debug == True:
                    print('Now Current User on the Login Page is %s %s' % (current_user.fname, current_user.lname))
                return redirect(url_for('index'))
            else:
                # Flash message
                return render_template('login.html', title='Login')
        # Sign up
        else:
            return render_template('signup.html', title='Sign up')
        
    # Show the login form
    else:
        return render_template('login.html', title='Login')
    
# Sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Do the login
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password']
        lname = request.form['lname']
        fname = request.form['fname']
        number = request.form['number']
        
        # Already signed up
        if email in total_users:
            # Flash message
            return render_template('signup.html', title='Sign up')
        # Sign up
        else:
            new_user = User(fname, lname, password, number, email)
            total_users.update({email: new_user})
            if app.debug == True:
                print('User signed up successfully - email: %s password: %s' % (email, password))
            return redirect(url_for('login'))
        
    # Show the Signup form
    else:
        return render_template('signup.html', title='signup')

    