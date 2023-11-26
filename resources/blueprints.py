from urllib.parse import urljoin
from flask import Blueprint, jsonify,render_template, request, redirect, url_for, current_app,session,flash
import pyodbc
from datetime import datetime
from resources import functions as F


login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.referrer != urljoin(request.url_root, url_for('login.login')):
        F.referral()
    if 'uid' in session:
        return redirect(session['url'])
    
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

addAuction_bp = Blueprint('addAuction', __name__)

@addAuction_bp.route('/addAuction', methods=['GET', 'POST'])
def addAuction():
    db_cursor = current_app.config['DB_CURSOR']

    # Get category details
    categories = F.categoryDetails(db_cursor, 0)

    # Get item statuses
    item_statuses = F.getStatusDefinitionswithGrp(db_cursor,'Item')

    if request.method == 'POST':
        # Retrieve form data
        item_name = request.form['Item_Name']
        item_img_path = request.form['Item_img_path']
        mrp = float(request.form['MRP'])
        seller_id = session['uid']
        item_desc = request.form['Item_desc']
        category_id = int(request.form['category_id'])
        item_status_id = int(request.form['Item_status'])
        auction_text = request.form['Auction_text']
        base_price = float(request.form['basePrice'])
        reserve_price = float(request.form['reservePrice'])
        bid_inc = float(request.form['bidInc'])
        start_date = datetime.strptime(request.form['startDate'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['endDate'], '%Y-%m-%dT%H:%M')

        try:
            
            # Execute the stored procedure
            db_cursor.execute("{CALL SP_insertAuctionItems (?,?,?,?,?,?,?,?,?,?,?,?,?)}",
                             item_name, item_img_path, mrp, seller_id, item_desc, category_id, item_status_id,
                             auction_text, base_price, reserve_price, bid_inc, start_date, end_date)
            
            db_cursor.commit()
            
            return redirect(url_for('myAuctions.myAuctions'))
        except Exception as e:
            db_cursor.rollback()
            return f'Error creating auction: {str(e)}'

    return render_template('addAuction.htm', categories=categories, item_statuses=item_statuses)


myBids_bp = Blueprint('myBids',__name__)

@myBids_bp.route('/myBids')
def myBids():
    db_cursor = current_app.config['DB_CURSOR']
    user_id = session.get('uid', None)
    db_cursor.execute("{CALL SP_getUserParticipatedAuctions(?)}", (user_id))
    myBids = db_cursor.fetchall()
    return render_template('myBids.htm', myBids=myBids)

@myBids_bp.route('/myBids/<int:auctionId>')
def get_bid_data(auctionId):
    db_cursor = current_app.config['DB_CURSOR']
    user_id = session.get('uid', None)
    db_cursor.execute("{CALL SP_getUserBidswithAuction(?,?)}", (user_id, auctionId))
    
    # Get column names from cursor.description
    column_names = [desc[0] for desc in db_cursor.description]
    
    # Convert rows to a list of dictionaries using column names
    bid_data = [dict(zip(column_names, row)) for row in db_cursor.fetchall()]
    
    return jsonify(bid_data)