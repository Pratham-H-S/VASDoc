from flask import Blueprint , render_template

Verify = Blueprint("Verify" , __name__, static_folder="static", template_folder="templates")

@Verify.route("/Verify")

def verify():
    return render_template("Verify.html")