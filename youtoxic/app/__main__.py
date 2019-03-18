from youtoxic.app.api.dash_layout import dash_layout
from youtoxic.app.api.file_layout import file_layout
from youtoxic.app.api.file_predictions import get_file_predictions
from youtoxic.app.api.text_layout import text_layout
from youtoxic.app.api.text_predictions import get_text_predictions
from youtoxic.app.api.tweet_layout import tweet_layout
from youtoxic.app.api.tweet_predictions import get_tweet_predictions

from youtoxic.app.context import create_pipeline

import dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html

import flask
from flask.helpers import get_root_path

from youtoxic.app.utils.neural_net import NeuralNet, Attention, Caps_Layer


meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

dash_app = dash.Dash(__name__,
                     url_base_pathname='/dash/',
                     assets_folder=get_root_path(__name__) + '/assets/',
                     meta_tags=[meta_viewport],
                     external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

dash_app.config['suppress_callback_exceptions'] = True
dash_app.title = 'YouToxic'
dash_app.layout = dash_layout

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def run():
    dash_app.run_server(debug=True)


def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        dash_layout,
        text_layout,
        tweet_layout
    ])


dash_app.layout = serve_layout
pipeline = create_pipeline()


@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
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
    if n_clicks is not None:
        return get_tweet_predictions(username, num_tweets, types, limit_date, start_date, end_date, pipeline)


@dash_app.callback(
    Output('date-picker', 'style'),
    [Input('limit-by-date', 'value')])
def toggle_date_picker(toggle_value):
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
    if contents is not None:
        return get_file_predictions(contents, filename, types, pipeline)


dash_app.run_server(debug=True)
