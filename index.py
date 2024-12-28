from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Veritabanı oluşturma ve örnek veri ekleme
def init_db():
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    c.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>Vulnerable Web App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: whitesmoke;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
            }
            .button {
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Vulnerable Web App</h1>
            <p>Go to the login page to test the SQL Injection vulnerability.</p>
            <a class="button" href="/login">Go To Login</a>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # SQL Injection açığı barındıran sorgu
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = sqlite3.connect('vulnerable.db')
        c = conn.cursor()
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return f"<h1>Welcome, {user[1]}!</h1>"
        else:
            return "<h1>Invalid credentials</h1>"

    return '''
    <html>
    <head>
        <title>Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: rgb(16, 129, 222);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            
            .text2 {
                margin-left: 65px;
            }
            
            .login-form {
                background: white;
                padding: 50px;
                border-radius: 10px 60px;
                box-shadow: 5px 4px 6px rgba(0, 0, 0, 0.1);
                width: 200px;
            }
            .login-form input {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .login-form button {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px;
                width: 100%;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            .login-form button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <form class="login-form" method="post">
            <h2 class="text2">Login</h2>
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
