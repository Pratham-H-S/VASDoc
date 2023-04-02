from flask import render_template , Blueprint

Approve = Blueprint("Approve" , __name__, static_folder="static" ,template_folder="templates")

@Approve.route('/Approve')

def approve():
    return render_template("Approve.html")
