from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret_key' # Change this to a secret key of your choice
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'lab3'

mysql = MySQL(app)

@app.route('/')
def index():
    # Check if user is logged in
    if 'user_id' in session:
        return 'Logged in as user {}'.format(session['user_id'])
    else:
        return 'Not logged in'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        dob = request.form['dob']
        
        # Check if email already exists in database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        if user:
            return 'Email already exists'
        
        # Insert new user into database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (name, email, password, phone, DOB) VALUES (%s, %s, %s, %s, %s)', (name, email, password, phone, dob))
        mysql.connection.commit()
        cur.close()
        
        return 'User registered successfully'
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        # Check if email and password match database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            # Store user ID in session
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
        else:
            return 'Incorrect email or password'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear session data
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()
    return render_template('home.html', posts=posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        likes = 0
        user_id = 1 # replace with actual user_id
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (user_id, title, description, likes) VALUES (%s, %s, %s, %s)", (user_id, title, description, likes))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    return render_template('add_post.html')

@app.route('/like_post/<int:post_id>')
def like_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE posts SET likes = likes + 1 WHERE post_id = %s", (post_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

@app.route('/add_comment/<int:post_id>', methods=['GET', 'POST'])
def add_comment(post_id):
    if request.method == 'POST':
        body = request.form['body']
        user_id = 1 # replace with actual user_id
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comments (user_id, post_id, body) VALUES (%s, %s, %s)", (user_id, post_id, body))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    return render_template('add_comment.html')