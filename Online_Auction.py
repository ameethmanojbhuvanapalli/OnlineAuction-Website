from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Define your database connection parameters
try:
    db_connection = pyodbc.connect(
        "Driver={ODBC Driver 11 for SQL Server};Server=AMEETHMANOJ;Database=Auction_DB;Trusted_Connection=yes"
    )
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")

db_cursor = db_connection.cursor()

@app.route('/')
def home():
    return 'Welcome to the login page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get email or phone number and password from the form
        loginID = request.form['email']
        password = request.form['password']

        # Call the stored procedure to check the user's credentials
        try:
            db_cursor.execute("{CALL SP_userLogin(?, ?)}", (loginID, password))
            result = db_cursor.fetchone()

            if result:
                user_id, user_name, role_id, role_name = result
                return f'Login successful! User ID: {user_id}, User Name: {user_name}, Role: {role_name}'
            else:
                return 'Login failed. Please try again.'
        except pyodbc.Error as e:
            print(f"Error calling the stored procedure: {e}")

    return render_template('login.htm') 

if __name__ == '__main__':
    app.run()
