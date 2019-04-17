"""For predicting the toxicities of texts given in file form."""

import base64
import io

import dash_html_components as html

import dash_table

import pandas as pd


def get_file_predictions(contents, filename, types, pipeline):
    """Returns the toxicity predictions for the texts contained in a csv or xls file.

    Parameters
    ----------
    contents: str
        Contents of the uploaded file.

    filename: str
        The name of the file.

    types: List
        The types of toxicity to predict for.

    pipeline: Object
        The pipeline object used to make predictions.

    Returns
    -------
        The html layout for the subsection of the page that contains results.

    """
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    df = None
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

    preds, judgements = dict(), dict()

    if "Toxicity" in types:
        preds["toxic"], judgements["toxic"] = pipeline.predict_toxicity_ulm_multiple(texts)
    if "Insult" in types:
        preds["insult"], judgements["insult"] = pipeline.predict_insult_multiple(texts)
    if "Obscenity" in types:
        preds["obscene"], judgements["obscene"] = pipeline.predict_obscenity_multiple(
            texts
        )
    if "Prejudice" in types:
        preds["prejudice"], judgements[
            "prejudice"
        ] = pipeline.predict_prejudice_multiple(texts)

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

    table_columns = [{"name": ["", "Text"], "id": "text"}]
    judgement_columns = [
        {"name": [t, "Judgement"], "id": "{}_judgement".format(t)} for t in types
    ]
    pred_columns = [
        {"name": [t, "Prediction"], "id": "{}_pred".format(t)} for t in types
    ]
    for judgement, pred in zip(judgement_columns, pred_columns):
        table_columns.append(judgement)
        table_columns.append(pred)

    return html.Div(
        [
            html.H5(filename),
            html.Div(
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=table_columns,
                    id="table",
                    style_table={"border": "thin black solid"},
                    style_header={
                        "fontWeight": "bold",
                        "backgroundColor": "rgb(150,150,150)",
                        "textAlign": "center",
                    },
                    style_cell={
                        "textAlign": "left",
                        "fontFamily": "optima",
                        "border": "thin lightgrey solid",
                        "padding": 15,
                    },
                    style_data={"whiteSpace": "normal"},
                    css=[
                        {
                            "selector": ".dash-cell div.dash-cell-value",
                            "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
                        }
                    ],
                    merge_duplicate_headers=True,
                    pagination_mode="fe",
                    pagination_settings={
                        "displayed_pages": 1,
                        "current_page": 0,
                        "page_size": 20,
                    },
                )
            ),
        ]
    )
