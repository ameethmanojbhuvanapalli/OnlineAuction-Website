import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'Item_img' not in request.files:
            return 'No file part'

        file = request.files['Item_img']

        # If the user does not select a file, browser also submits an empty part without filename
        if file.filename == '':
            return 'No selected file'

        if file:
            # Generate a unique filename based on the original filename
            filename = os.path.join('static/imgs/', secure_filename(file.filename))
            file.save(filename)
            return 'File uploaded successfully'

    return render_template("x.htm")
