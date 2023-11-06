from flask import Flask, render_template, session
import pyodbc
from resources import functions as F,blueprints as B

app = Flask(__name__)
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
    global role_id
    if 'uid' in session:
        user_id = session['uid']
        role_id = session.get('role_id',None)
    else:
        role_id=None
        print('not logged in')
        
@app.route('/')
def home():
    return render_template("index.htm",
        auctionData=F.getHomePageAuctions(app.config['DB_CURSOR'],3),
        functions=F.getRoleFunctions(app.config['DB_CURSOR'],role_id)) 



app.register_blueprint(B.login_bp)
app.register_blueprint(B.logout_bp)
app.register_blueprint(B.register_bp)
app.register_blueprint(B.auctionDetails_bp)

if __name__ == '__main__':
    app.run(debug=True)
