from software_project_manager import app

@app.route("/")
@app.route("/home")
@app.route("/index")
def home_page():
    return "<h1>Hello, World!</h1>"
