from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Set up database connection
client = MongoClient(
    'mongodb://localhost:27017')
db = client['mydatabase']

# Define sign-up page


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        if db.users.find_one({'email': email}):
            return 'User already exists'

        # Insert user data into database
        db.users.insert_one(
            {'name': name, 'email': email, 'password': password})

        return 'Sign up successful'

    # Render sign-up page
    return render_template('signup.html')


@app.route("/dashboard")
def dashboard():
    return 'Welcome to Dashboard'


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.users.find_one({'email': email})
        if user:
            if user['password'] == password:
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Credentials. Please try again.'
        else:
            error = 'User does not exist. Please sign up first.'
    return render_template('login.html', error=error)


app.run(host="localhost", port=8000)
