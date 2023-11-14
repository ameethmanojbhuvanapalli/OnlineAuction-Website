from urllib.parse import urljoin
from flask import Blueprint,render_template, request, redirect, url_for, current_app,session,flash
import pyodbc
from resources import functions as F


login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.referrer != urljoin(request.url_root, url_for('login.login')):
        session['url']=request.referrer
        if session['url'] == None:
            session['url'] = url_for('home')
    
    db_cursor = current_app.config['DB_CURSOR']
    if request.method == 'POST':
        loginID = request.form['email']
        password = request.form['password']

        try:
            db_cursor.execute("{CALL SP_userLogin(?, ?)}", (loginID, password))
            result = db_cursor.fetchone()

            if result:
                user_id, user_name, role_id, role_name = result
                session['uid']=user_id
                session['uname']=user_name
                session['role_id']=role_id
                return redirect(session['url'])
            else:
                flash('Login failed. Please try again.', 'error')
        except pyodbc.Error as e:
            print(f"Error calling the stored procedure: {e}")

    return render_template('login.htm')

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():

    if 'uid' in session:
        return redirect(url_for('home'))
    
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

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

auctionDetails_bp=Blueprint('auctionDetails',__name__)

@auctionDetails_bp.route('/auctionDetails/<int:aid>')
def auctionDetails(aid):
    db_cursor = current_app.config['DB_CURSOR']
    db_cursor.execute("{CALL SP_auctionDetailswithID(?)}",(aid))
    details = db_cursor.fetchone()
    db_cursor.execute("{CALL SP_bidHistorywithAuctionID(?)}",(aid))
    bidHistory = db_cursor.fetchall()
    return render_template('auctionDetails.htm',details=details,bidHistory=bidHistory)

@auctionDetails_bp.route('/addBid/<int:aid>',methods=['GET', 'POST'])
def addBid(aid):
    db_cursor = current_app.config['DB_CURSOR']
    bidamt = float(request.form['bid'])
    db_cursor.execute("{CALL SP_addBid(?,?,?)}",(session['uid'],aid,bidamt))
    db_cursor.commit()
    return redirect(url_for('auctionDetails.auctionDetails', aid=aid))

myAuctions_bp=Blueprint('myAuctions',__name__)

@myAuctions_bp.route('/myAuctions')
def myAuctions():
    db_cursor = current_app.config['DB_CURSOR']
    user_id = session.get('uid', None)
    db_cursor.execute("{CALL SP_getUserAuctions(?)}", (user_id))
    myAuctions = db_cursor.fetchall()
    return render_template('myAuctions.htm', myAuctions=myAuctions)

