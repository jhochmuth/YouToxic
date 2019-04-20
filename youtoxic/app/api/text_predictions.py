"""For predicting the toxicity of manually-entered text.

"""
import dash_html_components as html

from youtoxic.app.utils.create_dataframes import create_text_df
from youtoxic.app.utils.create_tables import create_text_table
from youtoxic.app.utils.predictions import make_predictions


def get_text_predictions(text, types, pipeline):
    """Returns the toxicity predictions for the entered text.

    Parameters
    ----------
    text : str
        The text to make a prediction for.
    types : list of str
        The types of toxicity to predict for.
    pipeline : Pipeline
        The pipeline object used to make predictions.

    Returns
    -------
    html.Div
        The html layout for the subsection of the page that contains results.

    """
    if not text:
        return html.Div(
            "Error: You must enter some text.", style={"color": "rgb(255, 0, 0"}
        )

    if not types:
        return html.Div(
            "Error: You must select at least one type of toxicity.",
            style={"color": "rgb(255, 0, 0"},
        )

    types_order, preds, judgements = make_predictions(text, types, pipeline)

    df = create_text_df(types_order, preds, judgements)

    table = create_text_table(df)

    return html.Div(
        [html.P("Text analyzed: {}".format(text), style={"marginBottom": "10"}), table]
    )
