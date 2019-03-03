from flask import render_template, redirect, url_for
from app import app
from app.forms import EnterTextForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home')


@app.route('/enter_text', methods=['GET', 'POST'])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        return redirect(url_for('analyze'))
    return render_template('enter_text.html', title='Enter Text', form=form)
