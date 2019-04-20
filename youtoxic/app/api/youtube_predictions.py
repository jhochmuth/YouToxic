import dash_html_components as html

from youtoxic.app.services.youtube_functionality import get_top_level_comments
from youtoxic.app.utils.create_dataframes import create_youtube_df
from youtoxic.app.utils.create_tables import create_file_table
from youtoxic.app.utils.predictions import make_predictions_multiple


def get_youtube_predictions(video_id, types, pipeline):
    comments = get_top_level_comments(video_id)

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

    preds, judgements = make_predictions_multiple(comments, types, pipeline)

    df = create_youtube_df(comments, types, preds, judgements)

    table = create_file_table(df, types)

    return html.Div(
        [
            html.Div(table, style={"overflowY": "scroll", "height": "500"}),
        ]
    )
