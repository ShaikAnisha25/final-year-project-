from flask import Flask, render_template, request, redirect, url_for, session
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from haar_removal import process_image  # Import hair removal function

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 🏠 Home Page
@app.route("/")
def index():
    return render_template("index.html")


# 📤 Upload Image for Hair Removal
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Process image for hair removal
            processed_filepath = process_image(filepath)

            return redirect(url_for("result", original=filepath, processed=processed_filepath))
    return render_template("upload.html")


# 📊 Result Page (Displays Processed Image)
@app.route("/result")
def result():
    original = request.args.get("original")
    processed = request.args.get("processed")
    if not original or not processed:
        return redirect(url_for("upload"))
    return render_template("result.html", original=original, processed=processed)


# 📧 Contact Page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        print(f"Received message from {name} ({email}): {message}")
        return "Message Sent Successfully!"
    return render_template("contact.html")


# 📝 User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session["user"] = email  # Simulate login session
        return redirect(url_for("index"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
