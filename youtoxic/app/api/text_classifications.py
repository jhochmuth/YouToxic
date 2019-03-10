from flask import render_template, session

from youtoxic.app.context import app, pipeline


@app.route("/text-classifications", methods=["GET"])
def get_text_classifications():
    """Calculates and displays predictions for text entered in /texts page."""
    preds = dict()
    classes = dict()
    pred_types = list()
    text = session["text"]
    if "toxic" in session["types"]:
        preds["Toxicity"], classes["Toxicity"] = pipeline.predict_toxicity(text)
        pred_types.append("Toxicity")
    if "identity" in session["types"]:
        preds["Identity hate"], classes[
            "Identity hate"
        ] = pipeline.predict_identity_hate(text)
        pred_types.append("Identity hate")
    if "obscene" in session["types"]:
        preds["Obscenity"], classes[
            "Obscenity"
        ] = pipeline.predict_obscenity(text)
        pred_types.append("Obscenity")
    session.pop("text", None)
    session.pop("types", None)
    return render_template(
        "text_classifications.html",
        title="Results",
        text=text,
        preds=preds,
        classes=classes,
        types=pred_types,
    )
