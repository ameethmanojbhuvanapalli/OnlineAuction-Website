from flask import Flask, render_template, session
import pyodbc
from blueprints import Functions as F

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

@app.route('/')
def home():
    auctionData = F.getHomePageAuctions(3)
    return render_template("index.htm",value=auctionData) 


app.register_blueprint(F.login_bp)
app.register_blueprint(F.register_bp)
app.register_blueprint(F.auctionDetails_bp)

if __name__ == '__main__':
    app.run(debug=True)
