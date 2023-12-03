from flask import Flask, jsonify, render_template, session
import pyodbc
from resources import functions as F,blueprints as B,x

app = Flask(__name__,static_folder='static')
app.secret_key = 'Ameeth'

# Define your database connection parameters
try:
    app.config['DB_CONNECTION'] = pyodbc.connect(
        "Driver={ODBC Driver 11 for SQL Server};Server=AMEETHMANOJ;Database=Auction_DB;Trusted_Connection=yes"
    )
    app.config['DB_CURSOR'] = app.config['DB_CONNECTION'].cursor()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")

@app.before_request
def check_session():
    global role_id,user_name,user_id
    if 'uid' in session:
        user_id = session.get('uid',None)
        user_name=session.get('uname',None)
        role_id = session.get('role_id',None)
    else:
        user_id=None
        user_name=None
        role_id=None
        
@app.route('/')
def home():
    return render_template(
        "index.htm",
        uname=user_name,
        auctionData=F.getHomePageAuctions(app.config['DB_CURSOR'], 3),
        functions=F.getRoleFunctions(app.config['DB_CURSOR'], role_id),
        categories=F.categoryDetails(app.config['DB_CURSOR'], 0)
    )

@app.route('/get_updated_auctions')
def get_updated_auctions():
    updated_auctions = F.getHomePageAuctions(app.config['DB_CURSOR'], 3)

    # Get column names from the cursor description
    columns = [column[0] for column in app.config['DB_CURSOR'].description]

    # Convert rows to dictionaries
    auctions_as_dicts = [dict(zip(columns, auction)) for auction in updated_auctions]

    return jsonify(auctions_as_dicts)

@app.route('/search/<string:auctionText>')
def search(auctionText):
    return render_template(
        "search.htm",
        auctionText=auctionText,
        auctionData=F.searchAuctions(app.config['DB_CURSOR'], auctionText),
        functions=F.getRoleFunctions(app.config['DB_CURSOR'], role_id),
    )

@app.route('/category/<int:catid>')
def category(catid):
    return render_template(
        "categoryProducts.htm",
        category=F.categoryDetails(app.config['DB_CURSOR'], catid),
        auctionData=F.getCategoryAuctions(app.config['DB_CURSOR'], catid),
        functions=F.getRoleFunctions(app.config['DB_CURSOR'], role_id),
    )



app.register_blueprint(B.login_bp)
app.register_blueprint(B.logout_bp)
app.register_blueprint(B.register_bp)
app.register_blueprint(B.auctionDetails_bp)
app.register_blueprint(B.myAuctions_bp)
app.register_blueprint(B.addAuction_bp)
app.register_blueprint(B.myBids_bp)
app.register_blueprint(B.payment_bp)

app.register_blueprint(x.upload_bp)

if __name__ == '__main__':
    app.run(debug=True)
