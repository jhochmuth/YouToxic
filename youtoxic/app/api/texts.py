from flask import flash, redirect, render_template, session, url_for

from youtoxic.app.context import app
from youtoxic.app.api.forms import EnterTextForm


@app.route('/texts', methods=['GET'])
def get_texts():
    form = EnterTextForm()
    return render_template('enter_text.html', title='Enter Text', form=form)


@app.route('/texts', methods=['POST'])
def post_texts():
    form = EnterTextForm()
    if form.validate_on_submit():
        if len(form.text.data.split()) < 3:
            flash('Warning: accuracy of predictions is low for texts with few words.')
        session['text'] = form.text.data
        session['types'] = form.types.data
        return redirect(url_for('get_text_classifications'))
    flash('Error: no data entered.')
    return redirect(url_for('get_texts'))
