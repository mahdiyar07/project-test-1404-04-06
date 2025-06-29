from flask import Flask, render_template, request, flash, redirect
import os
import chenge  # فایل chenge.py را ایمپورت می‌کنیم

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200 مگابایت
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('هیچ فایلی انتخاب نشده است.', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('فقط فایل‌های PDF مجاز هستند.', 'danger')
            return redirect(request.url)

        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            flash('حجم فایل نباید بیش از 200 مگابایت باشد.', 'danger')
            return redirect(request.url)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # فراخوانی تابع تبدیل PDF به Word
        result = chenge.process_uploaded_file(file_path)

        if result:
            flash('فایل با موفقیت آپلود و به ورد تبدیل شد.', 'success')
        else:
            flash('خطا در تبدیل فایل PDF به Word.', 'danger')

        return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
