from flask import Blueprint, render_template, request, redirect, url_for, current_app
import pyodbc

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    db_cursor = current_app.config['DB_CURSOR']

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

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    db_cursor = current_app.config['DB_CURSOR']

    if request.method == 'POST':
        # Get user registration data from the form
        usr_name = request.form['usr_name']
        email = request.form['email']
        DOB = request.form['DOB']
        phno = request.form['phno']
        house_no = request.form['house_no']
        street = request.form['street']
        city = request.form['city']
        pin_code = request.form['pin_code']
        pwd = request.form['pwd']

        try:
            db_cursor.execute("{CALL SP_registerUser(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}",
                             (usr_name, email, DOB, phno, house_no, street, city, pin_code, pwd, 1003))
            db_cursor.commit()

            return redirect(url_for('login.login'))
        except pyodbc.Error as e:
            print(f"Error calling the stored procedure: {e}")

    return render_template('register.htm')
