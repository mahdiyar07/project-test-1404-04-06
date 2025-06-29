from flask import Flask, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret123'  # برای flash message
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# بررسی فرمت
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('فایلی انتخاب نشده است.')
            return redirect(request.url)
        file = request.files['pdf_file']
        if file.filename == '':
            flash('هیچ فایلی انتخاب نشده است.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash('فایل با موفقیت ذخیره شد!')
            return redirect(request.url)
        else:
            flash('فقط فایل‌های PDF مجاز هستند.')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
