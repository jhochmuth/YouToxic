"""Contains routes for the flask app.

"""
from flask import Blueprint, render_template


main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
@main_bp.route("/index")
def index():
    return render_template("index.html", title="YouToxic", template="home_template")
