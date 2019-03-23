"""Defines page layout for home/index page."""

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
        dcc.Link(
            "Analyze text by manual entry",
            href="/texts",
            style={"color": "rgb(0, 0, 0)"},
        ),
        html.Br(),
        dcc.Link(
            "Analyze tweets of a Twitter user",
            href="/tweets",
            style={"color": "rgb(0, 0, 0)"},
        ),
        html.Br(),
        dcc.Link(
            "Analyze texts of a file", href="/files", style={"color": "rgb(0, 0, 0)"}
        ),
    ]
)
