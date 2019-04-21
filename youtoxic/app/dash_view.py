"""Contains the functioning of the dash app.

"""
from dash import Dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc

import dash_html_components as html

from youtoxic.app.api.dash_layout import dash_layout
from youtoxic.app.api.file_layout import file_layout
from youtoxic.app.api.file_predictions import get_file_predictions
from youtoxic.app.api.text_layout import text_layout
from youtoxic.app.api.text_predictions import get_text_predictions
from youtoxic.app.api.tweet_layout import tweet_layout
from youtoxic.app.api.tweet_predictions import get_tweet_predictions
from youtoxic.app.api.youtube_layout import youtube_layout
from youtoxic.app.api.youtube_predictions import get_youtube_predictions
from youtoxic.app.services.pipeline import Pipeline


url_bar_and_content_div = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


def add_dash(server):
    """Initializes the Dash app.

    Parameters
    ----------
    server : Flask
        The Flask app that serves the Dash app.

    Returns
    -------
    Flask
        The server of the Dash app.

    """
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    dash_app = Dash(
        __name__,
        server=server,
        assets_folder="assets/",
        external_stylesheets=external_stylesheets,
        routes_pathname_prefix="/dash/",
    )

    dash_app.layout = dash_layout
    dash_app.config["suppress_callback_exceptions"] = True
    pipeline = Pipeline()

    @dash_app.callback(Output("content", "children"), [Input("tabs", "value")])
    def display_page(tab):
        """Callback function to inform app of which tab to display.

        Parameters
        ----------
        tab : str
            The value of the tab to display.

        Returns
        -------
        html.Div
            The layout corresponding to the requested tab.

        """
        if tab == "tweet-predictions":
            return tweet_layout
        elif tab == "youtube-predictions":
            return youtube_layout
        elif tab == "text-predictions":
            return text_layout
        elif tab == "file-predictions":
            return file_layout
        else:
            return dash_layout

    @dash_app.callback(
        Output("text-container", "children"),
        [Input("button", "n_clicks")],
        [State("input-text", "value"), State("types", "values")],
    )
    def update_text_output(n_clicks, text, types):
        """Callback function to display prediction results of manual text entry.

        Parameters
        ----------
        n_clicks : int
            Number of times 'Submit' has been clicked. Set to None until user has clicked 'Submit' at least once.
        text : str
            The text to make a prediction for.
        types : list of str
            The types of toxicity to predict for.

        Returns
        -------
        html.Div
           The html layout for the subsection of the page that contains results.

        """
        if n_clicks is not None:
            return get_text_predictions(text, types, pipeline)

    @dash_app.callback(
        Output("tweet-container", "children"),
        [Input("button", "n_clicks")],
        [
            State("input-text", "value"),
            State("input-num", "value"),
            State("types", "values"),
            State("limit-by-date", "value"),
            State("date-picker", "start_date"),
            State("date-picker", "end_date"),
        ],
    )
    def update_tweet_output(
        n_clicks, username, num_tweets, types, limit_date, start_date, end_date
    ):
        """Callback function to display prediction results of a Twitter username search.

        Parameters
        ----------
        n_clicks : int
            Number of times 'Submit' has been clicked. Set to None until user has clicked 'Submit' at least once.
        username : str
            Tweets will be collected from this user.
        num_tweets : int
            The maximum number of tweets to analyze.
        types : list of str
            The types of toxicity to predict for.
        limit_date : str
            Whether to get tweets between a certain date range ('date') or the most recent tweets ('all').
        start_date : Datetime
            The beginning value of the date range. Only matters if limit_date == 'date'.
        end_date : Datetime
            The ending value of the date range. Only matters if limit_date == 'date'.

        Returns
        -------
        html.Div
           The html layout for the subsection of the page that contains results.

        """
        if n_clicks is not None:
            return get_tweet_predictions(
                username, num_tweets, types, limit_date, start_date, end_date, pipeline
            )

    @dash_app.callback(
        Output("date-picker", "style"), [Input("limit-by-date", "value")]
    )
    def toggle_date_picker(toggle_value):
        """Callback function to inform app if tweet_layout should display date range selector.

        Parameters
        ----------
        toggle_value : str
            Whether to display date range selector ('date') or not ('all').

        Returns
        -------
        dict
            Display is set to 'block' if date range selector should be displayed, 'none' otherwise.

        """
        if toggle_value == "date":
            return {"display": "block"}
        else:
            return {"display": "none"}

    @dash_app.callback(
        Output("youtube-container", "children"),
        [Input("button", "n_clicks")],
        [
            State("input-text", "value"),
            State("types", "values"),
        ],
    )
    def update_tweet_output(
        n_clicks, video_id, types
    ):
        """Callback function to display prediction results of a Twitter username search.

        Parameters
        ----------
        n_clicks : int
            Number of times 'Submit' has been clicked. Set to None until user has clicked 'Submit' at least once.
        video_id : str
            Tweets will be collected from this user.
        types : list of str
            The types of toxicity to predict for.

        Returns
        -------
        html.Div
           The html layout for the subsection of the page that contains results.

        """
        if n_clicks is not None:
            return get_youtube_predictions(
                video_id, types, pipeline
            )

    @dash_app.callback(
        Output("file-container", "children"),
        [Input("upload-data", "contents")],
        [State("upload-data", "filename"), State("types", "values")],
    )
    def update_file_output(contents, filename, types):
        """Callback function to display prediction results of file analysis.

        Parameters
        ----------
        contents : str
            Contents of the uploaded file.
        filename : str
            The name of the file.
        types : list of str
            The types of toxicity to predict for.

        Returns
        -------
        html.Div
            The html layout for the subsection of the page that contains results.

        """
        if contents is not None:
            return get_file_predictions(contents, filename, types, pipeline)

    return dash_app.server
