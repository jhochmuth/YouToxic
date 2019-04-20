"""For predicting the toxicities of texts given in file form.

"""
import base64
import io

import dash_html_components as html

import pandas as pd

from youtoxic.app.utils.create_tables import create_file_table
from youtoxic.app.utils.predictions import make_predictions_multiple


def get_file_predictions(contents, filename, types, pipeline):
    """Returns the toxicity predictions for the texts contained in a csv or xls file.

    Parameters
    ----------
    contents : str
        Contents of the uploaded file.
    filename : str
        The name of the file.
    types : list of str
        The types of toxicity to predict for.
    pipeline : Pipeline
        The pipeline object used to make predictions.

    Returns
    -------
    html.Div
        The html layout for the subsection of the page that contains results.

    """
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), index_col=False)
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div(
                ["Error: File given must be in csv or xls format."],
                style={"color": "rgb(250, 0, 0)"},
            )

    except Exception as e:
        print(e)
        return html.Div(
            ["There was an error processing this file."],
            style={"color": "rgb(250, 0, 0)"},
        )

    texts = df["text"].values

    preds, judgements = make_predictions_multiple(texts, types, pipeline)

    if "Toxicity" in types:
        df["Toxicity_judgement"] = judgements["toxic"]
        df["Toxicity_pred"] = preds["toxic"]
        df["Toxicity_pred"] = df["Toxicity_pred"].map("{:.3f}".format)
    if "Insult" in types:
        df["Insult_judgement"] = judgements["insult"]
        df["Insult_pred"] = preds["insult"]
        df["Insult_pred"] = df["Insult_pred"].map("{:.3f}".format)
    if "Obscenity" in types:
        df["Obscenity_judgement"] = judgements["obscene"]
        df["Obscenity_pred"] = preds["obscene"]
        df["Obscenity_pred"] = df["Obscenity_pred"].map("{:.3f}".format)
    if "Prejudice" in types:
        df["Prejudice_judgement"] = judgements["prejudice"]
        df["Prejudice_pred"] = preds["prejudice"]
        df["Prejudice_pred"] = df["Prejudice_pred"].map("{:.3f}".format)

    graph = create_file_table(df, types)

    return html.Div(
        [
            html.H5(filename),
            html.Div(graph)
        ]
    )
