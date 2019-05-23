"""Defines page layout for home/index page.

"""
import dash_core_components as dcc

import dash_html_components as html


dash_layout = html.Div(
    [
        html.Div(
            [
                html.H2("YouToxic"),
                html.Img(src="assets/logo.png"),
            ],
            className="banner",
        ),
        dcc.Tabs(
            id="tabs",
            value="tweet-predictions",
            children=[
                dcc.Tab(label="Tweet Predictions", value="tweet-predictions"),
                dcc.Tab(label="Youtube Comment Predictions", value="youtube-predictions"),
                dcc.Tab(label="Text Predictions", value="text-predictions"),
                dcc.Tab(label="File Predictions", value="file-predictions"),
            ],
        ),
        html.Div(id="content"),
    ],
    style={
        "marginLeft": 10,
        "marginRight": 10,
        "marginBottom": 20,
    }
)
