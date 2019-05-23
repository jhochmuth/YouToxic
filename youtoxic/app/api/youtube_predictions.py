import dash_html_components as html

from youtoxic.app.services.youtube_comment_dumper import get_top_level_comments
from youtoxic.app.utils.create_dataframes import create_youtube_df
from youtoxic.app.utils.create_graphs import create_average_toxicity_graph, create_violin_plot
from youtoxic.app.utils.create_tables import create_youtube_table
from youtoxic.app.utils.predictions import make_predictions_multiple


def get_youtube_predictions(video_id, types, pipeline):
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
            html.Div(table, className="six columns", style={"overflow": "scroll", "height": 920}),
            html.Div(graph, className="six columns", style={"marginBottom": 20}),
            html.Div(plot, className="six columns"),
        ],
        className="row",
        style={"marginBottom": 20},
    )
