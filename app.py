from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

rescue_requests = []  # Temporary in-memory storage

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    return render_template('index.html', requests=rescue_requests)

@app.route('/rescue', methods=['GET', 'POST'])
def rescue():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        location = request.form['location']
        description = request.form['description']
        file = request.files['image']

        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(datetime.utcnow().strftime("%Y%m%d%H%M%S_") + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        rescue_requests.append({
            "name": name,
            "phone": phone,
            "location": location,
            "description": description,
            "image": filename
        })
        return redirect(url_for('index'))
    return render_template('rescue.html')

if __name__ == "__main__":
    app.run(debug=True)
