"""Contains functionality for running the app."""

import dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html

import flask
from flask.helpers import get_root_path

from youtoxic.app.api.dash_layout import dash_layout
from youtoxic.app.api.file_layout import file_layout
from youtoxic.app.api.file_predictions import get_file_predictions
from youtoxic.app.api.text_layout import text_layout
from youtoxic.app.api.text_predictions import get_text_predictions
from youtoxic.app.api.tweet_layout import tweet_layout
from youtoxic.app.api.tweet_predictions import get_tweet_predictions
from youtoxic.app.services.pipeline import Pipeline
from youtoxic.app.utils.neural_net import NeuralNet, Attention, Caps_Layer


def create_server():
    """Creates the dash app instance."""
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    app = dash.Dash(__name__,
                    url_base_pathname='/dash/',
                    assets_folder=get_root_path(__name__) + '/assets/',
                    meta_tags=[meta_viewport],
                    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

    app.config['suppress_callback_exceptions'] = True
    app.title = 'YouToxic'
    app.layout = dash_layout

    return app


def create_pipeline():
    """Creates the pipeline object."""
    return Pipeline()


url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def serve_layout():
    """Serves general layout to dash app."""
    if flask.has_request_context():
        return url_bar_and_content_div

    else:
        return html.Div([
            url_bar_and_content_div,
            dash_layout,
            text_layout,
            tweet_layout
        ])


dash_app = create_server()
dash_app.layout = serve_layout
pipeline = create_pipeline()


@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    """Callback function to inform app of which page to display.

    Parameters
    ----------
    pathname: str
        The pathname of the page to display.

    Returns
    -------
        The layout corresponding to the requested pathname.

    """
    if pathname == '/texts':
        return text_layout
    if pathname == '/tweets':
        return tweet_layout
    if pathname == '/files':
        return file_layout
    else:
        return dash_layout


@dash_app.callback(
    Output('text-container', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-text', 'value'), State('types', 'values')])
def update_output(n_clicks, text, types):
    """Callback function to display prediction results of manual text entry.

    Parameters
    ----------
    n_clicks: int
        Number of times 'Submit' has been clicked. Set to None until user has clicked 'Submit' at least once.

    text: str
        The text to make a prediction for.

    types:
        The types of toxicity to predict for.

    Returns
    -------
       The html layout for the subsection of the page that contains results.

    """
    if n_clicks is not None:
        return get_text_predictions(text, types, pipeline)


@dash_app.callback(
    Output('tweet-container', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-text', 'value'),
     State('input-num', 'value'),
     State('types', 'values'),
     State('limit-by-date', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')])
def update_output(n_clicks, username, num_tweets, types, limit_date, start_date, end_date):
    """Callback function to display prediction results of a Twitter username search.

    Parameters
    ----------
    n_clicks: int
        Number of times 'Submit' has been clicked. Set to None until user has clicked 'Submit' at least once.

    username: str
        The Twitter user to collect tweets from.

    num_tweets: int
        The maximum number of tweets to analyze.

    types:
        The types of toxicity to predict for.

    limit_date: str
        Whether to get tweets between a certain date range ('date') or the most recent tweets ('all').

    start_date: Datetime
        The beginning value of the date range. Only matters if limit_date == 'date'.

    end_date: Datetime
        The ending value of the date range. Only matters if limit_date == 'date'.

    Returns
    -------
       The html layout for the subsection of the page that contains results.

    """
    if n_clicks is not None:
        return get_tweet_predictions(username, num_tweets, types, limit_date, start_date, end_date, pipeline)


@dash_app.callback(
    Output('date-picker', 'style'),
    [Input('limit-by-date', 'value')])
def toggle_date_picker(toggle_value):
    """Callback function to inform app if tweet_layout should display date range selector.

    Parameters
    ----------
    toggle_value: str
        Whether to display date range selector ('date') or not ('all').

    Returns
    -------
    dict
        Display is set to 'block' if date range selector should be displayed, 'none' otherwise.

    """
    if toggle_value == 'date':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@dash_app.callback(
    Output('file-container', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('types', 'values')]
)
def update_output(contents, filename, types):
    """Callback function to display prediction results of file analysis.

    Parameters
    ----------
    contents: str
        Contents of the uploaded file.

    filename: str
        The name of the file.

    types: List
        The types of toxicity to predict for.

    Returns
    -------
        The html layout for the subsection of the page that contains results.

    """
    if contents is not None:
        return get_file_predictions(contents, filename, types, pipeline)


dash_app.run_server(debug=True)
