from flask import redirect, render_template, url_for

from toxicity_analysis.app.context import app
from toxicity_analysis.app.forms import EnterTextForm


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Home")


@app.route("/enter_text", methods=["GET", "POST"])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        return redirect(url_for("analyze"))
    return render_template("enter_text.html", title="Enter Text", form=form)
