import fitz  # PyMuPDF
import os

def process_uploaded_file(file_path):
    try:
        pdf = fitz.open(file_path)
        output_path = os.path.splitext(file_path)[0] + '.doc'

        html_content = "<html><body dir='rtl' style='font-family:Tahoma;'>\n"
        for page in pdf:
            text = page.get_text("text")
            text = text.replace('\n', '<br>')
            html_content += f"<p>{text}</p>\n"
        html_content += "</body></html>"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ فایل ورد ساده ساخته شد: {output_path}")
        return True
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False
