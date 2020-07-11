from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import os

app = Flask(__name__)
dropzone = Dropzone(app)
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'

def human(size):
    B = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"
    UNITS = [B, KB, MB, GB, TB]
    HUMANFMT = "%.2f %s"
    HUMANRADIX = 1024.

    for u in UNITS[:-1]:
        if size < HUMANRADIX : return HUMANFMT % (size, u)
        size /= HUMANRADIX

    return HUMANFMT % (size,  UNITS[-1])

@app.route("/")
def main():
    return render_template('index.html', the_title="Home")

@app.route("/gallery")
def gallery():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path_folder=os.path.join(dir_path, 'static')
    list_images = []
    if os.path.isdir(path_folder):
        list_files = os.listdir(path_folder)
        for file in list_files:
            path_file = os.path.join(path_folder, file)
            size_o_file = os.stat(path_file).st_size
            tuple_item = (file, human(size_o_file))
            list_images.append(tuple_item)
    list_images.sort(key=lambda elem: elem[1], reverse=True)
    return render_template('gallery.html', the_title="Gallery", list_images=list_images)

@app.route('/about')
def about():
    return render_template('about.html', the_title="About",site_desc='hello\naaaaaa')

@app.route('/uploads', methods=['GET', 'POST'])
def upload():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    UPLOADED_PATH=os.path.join(dir_path, 'static')
    if not os.path.exists(UPLOADED_PATH):
        os.mkdir(UPLOADED_PATH)
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(UPLOADED_PATH, f.filename))

    return 'upload template'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')