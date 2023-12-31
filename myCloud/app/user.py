import itertools

global total_users
total_users = {}

class User:
    auto_id = itertools.count()
    def __init__(self, fname='First name', lname='Last name', password='password', 
                 number='number', email='email'):
        self.fname = fname
        self.lname = lname
        self.id = next(self.auto_id)
        self.number = number
        self.email = email
        self.password = password
        self.logged_in = False
    
    def login(self, email, password):
        if password == self.password:
            self.logged_in = True
        else:
            self.logged_in = False
        return self.logged_in