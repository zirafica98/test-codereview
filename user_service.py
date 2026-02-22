import mysql.connector
import subprocess
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hardkodovani credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password123',  # Hardkodovana lozinka
    'database': 'testdb'
}

# SQL Injection - direktna konkatenacija korisničkog inputa
def get_user_by_username(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)  # SQL injection!
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Još jedna SQL injection greška
def delete_user(user_id):
    sql = f"DELETE FROM users WHERE id = {user_id}"
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(sql)  # SQL injection!
    conn.commit()
    cursor.close()
    conn.close()

# XSS vulnerability - direktan output bez sanitizacije
@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form.get('comment')
    template = f"<div>{comment}</div>"  # XSS!
    return render_template_string(template)

# Command injection
def execute_command(user_input):
    subprocess.call(['ping', user_input])  # Command injection!
    # Ili još gore:
    os.system(f"ping {user_input}")  # Command injection!

# Hardkodovani secret key
SECRET_KEY = "mySecretKey123"  # Hardkodovani secret

# Loša praksa - slanje lozinke u plain text-u
def login(username, password):
    # Nema hash-ovanja lozinke
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    # SQL injection + plain text password!
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# Nema validacije inputa
def process_payment(amount, card_number):
    # Nema validacije
    payment_data = {
        'amount': amount,
        'card_number': card_number
    }
    # Slanje payment podataka...

# Loša praksa - eval sa korisničkim inputom
def calculate_expression(expression):
    result = eval(expression)  # Opasno! Eval sa korisničkim inputom
    return result

# Loša praksa - pickle sa nevalidiranim podacima
import pickle
def load_user_data(data):
    user = pickle.loads(data)  # Opasno! Pickle može izvršiti kod
    return user

if __name__ == '__main__':
    app.run(debug=True)  # Debug mode u produkciji - loša praksa
