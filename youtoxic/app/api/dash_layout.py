"""Defines page layout for home/index page.

"""
import dash_core_components as dcc

import dash_html_components as html


dash_layout = html.Div(
    [
        html.Div(
            [
                html.H2("YouToxic", style={"color": "rgb(200, 200, 200)"}),
                html.Img(src="assets/image-2.png"),
            ],
            style={"fontFamily": "arial black"},
            className="banner",
        ),
        dcc.Tabs(
            id="tabs",
            value="tweet-predictions",
            children=[
                dcc.Tab(label="Tweet Predictions", value="tweet-predictions"),
                dcc.Tab(label="Text Predictions", value="text-predictions"),
                dcc.Tab(label="File Predictions", value="file-predictions"),
            ],
        ),
        html.Div(id="content"),
    ]
)
