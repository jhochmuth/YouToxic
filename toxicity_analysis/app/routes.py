from flask import flash, redirect, render_template, url_for

from toxicity_analysis.app.context import app
from toxicity_analysis.app.forms import EnterTextForm
from toxicity_analysis.app.predict_toxicity import predict_toxicity


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/enter_text", methods=["GET", "POST"])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        if len(form.text.data.split()) < 3:
            flash('Warning: predicted accuracy is low for text with low word count.')
        return redirect(url_for("results", text=form.text.data))
    return render_template("enter_text.html", title="Enter Text", form=form)


@app.route("/results/<text>")
def results(text):
    prediction = predict_toxicity(text)
    return render_template("results.html", title="Results", text=text, prediction=prediction)
