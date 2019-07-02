import re

import dash_html_components as html

from youtoxic.app.services.youtube_comment_dumper import get_top_level_comments
from youtoxic.app.utils.create_dataframes import create_youtube_df
from youtoxic.app.utils.create_graphs import create_average_toxicity_graph, create_violin_plot
from youtoxic.app.utils.create_tables import create_youtube_table
from youtoxic.app.utils.predictions import make_predictions_multiple


def get_youtube_predictions(video_id, types, pipeline):
    """Collects youtube comments, analyzes them, and creates a table and a line graph.

    Parameters
    ----------
    video_id : str
        Tweets will be collected from the video with this id or url.
    types : list of str
        Predictions will be made for these types of toxicity
    pipeline : Pipeline
        The pipeline object used to make predictions.

    Returns
    -------
    html.Div
        The html layout for the subsection of the page that contains results.
    """
    if "youtube" in video_id:
        try:
            m = re.search("v=(\w+)&*", video_id)
            video_id = m.group(1)
        except AttributeError:
            return html.Div(
                "Error: Could not parse given URL.",
                style={"color": "rgb(255, 0, 0"},
            )

    comments, authors, times = get_top_level_comments(video_id)

    if comments is None:
        return html.Div(
            "Error: No video with the specified id was found.",
            style={"color": "rgb(255, 0, 0"},
        )

    if len(comments) == 0:
        return html.Div(
            "Error: A video matching the specified id was found, but it contained no comments.",
            style={"color": "rgb(255, 0, 0"},
        )

    comments = [comment for time, comment in sorted(zip(times, comments))]
    authors = [author for time, author in sorted(zip(times, authors))]
    times = sorted(times)

    preds, judgements = make_predictions_multiple(comments, types, pipeline)

    df = create_youtube_df(comments, authors, times, types, preds, judgements)
    table = create_youtube_table(df, types)
    graph = create_average_toxicity_graph(times, types, preds)
    plot = create_violin_plot(types, preds)

    return html.Div(
        [
            html.Div(table, className="six columns", style={"overflow": "scroll", "height": 922}),
            html.Div(graph, className="six columns", style={"marginBottom": 20}),
            html.Div(plot, className="six columns"),
        ],
        className="row",
        style={"marginBottom": 20},
    )
