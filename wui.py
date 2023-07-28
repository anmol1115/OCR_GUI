import os
from utils import create_project_fs
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "./images"
ALLOWED_EXTENSION = ["png", "jpg", "jpeg"]

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No File uploaded")
            return redirect(request.url)
        file = request.files.get("file")
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(request.url)
    if request.method == "GET":
        return render_template("upload.html")

if __name__ == "__main__":
    create_project_fs()
    app.run(host="0.0.0.0", port=8080)