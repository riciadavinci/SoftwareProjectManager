from flask import render_template
from software_project_manager import app


@app.route("/home")
@app.route("/index")
@app.route("/")
def home_page():
    return render_template("login.html")

@app.route("/login")
def login_page():
    
    return render_template("login.html")
