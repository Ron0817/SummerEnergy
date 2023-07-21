from flask import render_template, url_for, request, redirect, flash, session
from markupsafe import escape
from app import app
from app.user import User, total_users

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
    if 'email' in session:
        current_user = total_users[session['email']]
        if app.debug == True:
            print('TOTAL USER LIST: {}'.format(total_users))
        return render_template('index.html', title='Home', user=current_user, posts=posts)
    else:
        return render_template('index.html', title='Home', user=User('Please log in'), posts=posts)

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
            flash('Sign up first.')
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
            flash('Email already signed up. Try log in.')
            return redirect(url_for('login'))
        # Sign up
        else:
            new_user = User(fname, lname, password, number, email)
            total_users.update({email: new_user})
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
        total_users.pop(session['email'])
        session.pop('email')
    else:
        flash("You are logged out")
    return redirect(url_for('index'))