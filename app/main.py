from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, session, url_for
import hashlib
from datetime import timedelta
from utils import get_db
from pydantic import BaseModel
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)


db = get_db()

# pydantic models

class User(BaseModel):
    username: str
    password: str



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user_profile = db.users.find_one({"username": username, "password": password}, projection={"_id": False})
    
        if user_profile:
            user_profile = User.parse_obj(user_profile)
            logging.info(f"Logging user = {user_profile.username}")
            session.permanent = True
            session["user"] = user_profile.dict()
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("login"))
    
    if request.method == "GET":
        flash_msg = get_flashed_messages()
        return render_template("login.html", flash_msg=flash_msg)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/new_post")
def add_post():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("new_post.html")


if __name__ == "__main__":
    app.run(debug=True)
