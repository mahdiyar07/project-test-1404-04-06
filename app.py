from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # برای پیام‌های flash ضروری است

# تنظیم مسیر ذخیره فایل‌ها
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# حداکثر حجم فایل (1 مگابایت)
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('هیچ فایلی انتخاب نشده است.', 'danger')
            return redirect(request.url)

        # بررسی حجم فایل
        file.seek(0, os.SEEK_END)  # حرکت به انتهای فایل
        file_length = file.tell()
        file.seek(0)  # بازگشت به ابتدای فایل

        if file_length > MAX_FILE_SIZE:
            flash('حجم فایل نباید بیش از 1 مگابایت باشد.', 'danger')
            return redirect(request.url)

        # ذخیره فایل
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash('فایل با موفقیت آپلود شد.', 'success')
        return redirect(request.url)

    return render_template('index.html')
