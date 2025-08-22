from flask import render_template, redirect, send_from_directory, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from software_project_manager import app
from .models import User
from .forms import LoginForm
from .app_wrappers import jwt_view_required


@app.route("/home")
@app.route("/index")
@app.route("/")
@jwt_view_required
def home_page():
    return redirect(url_for("login_page"))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/robots.txt")
def view_robots_txt_file():
    try:
        return send_from_directory("static", "misc/robots.txt")
    except:
        return "<h1>404, Not found!</h1>"

@app.route("/kanban-board")
@jwt_view_required
def view_kanban_board():
    
    return render_template("kanban_Board.html")
