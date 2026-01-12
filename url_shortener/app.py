from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string
import re

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Table definition
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), nullable=False, unique=True)

with app.app_context():
    db.create_all()

def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)?'
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'
        r'(:\d+)?(/.*)?$'
    )
    return re.match(pattern, url)

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = ""
    error = ""

    if request.method == "POST":
        long_url = request.form.get("long_url")

        if not is_valid_url(long_url):
            error = "Please enter a valid URL"
        else:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            short_url = f"http://127.0.0.1:5000/{code}"

            new_url = URL(original_url=long_url, short_code=code)
            db.session.add(new_url)
            db.session.commit()

    return render_template("home.html", short_url=short_url, error=error)

@app.route("/<code>")
def redirect_to_url(code):
    record = URL.query.filter_by(short_code=code).first()
    if record:
        return redirect(record.original_url)
    return "Invalid URL"

@app.route("/history")
def history():
    all_urls = URL.query.all()
    return render_template("history.html", urls=all_urls)

if __name__ == "__main__":
    app.run(debug=True)
