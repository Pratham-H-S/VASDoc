from flask import Flask , Blueprint , render_template

Profile = Blueprint("Profile", __name__, static_folder= "static", template_folder="template")

@Profile.route("/Profile")
def profile():
    return render_template("Profile.html")