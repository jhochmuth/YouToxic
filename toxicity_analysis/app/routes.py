from flask import redirect, render_template, url_for

from toxicity_analysis.app.context import app
from toxicity_analysis.app.forms import EnterTextForm


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/enter_text", methods=["GET", "POST"])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        return redirect(url_for("results"))
    return render_template("enter_text.html", title="Enter Text", form=form)


@app.route("/results")
def results():
    return render_template("results.html", title="Results", result=0)
