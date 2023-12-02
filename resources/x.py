import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/x', methods=['GET', 'POST'])
def upload_file():
    db_cursor = current_app.config['DB_CURSOR']
    db_cursor.execute("{CALL SP_auctionDetailswithID(?)}",(9))
    details=db_cursor.fetchone()
    return render_template("x.htm",details=details)
