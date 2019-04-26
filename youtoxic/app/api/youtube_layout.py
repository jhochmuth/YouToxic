"""Defines page layout for analysis of tweets.

"""
import dash_core_components as dcc

import dash_html_components as html


youtube_layout = html.Div(
    [
        html.Details(
            [
                html.Summary(
                    "Click here to view instructions.", style={"color": "rgb(0,0,0"}
                ),
                html.Div(
                    "– Enter ID of Youtube video."
                ),
                html.Div("– Select types of toxicity to analyze comments for."),
            ],
            style={"color": "rgb(175, 175, 175", "marginBottom": "20"},
        ),
        dcc.Loading(id="loading-1",
                    children=html.Div(id="youtube-container",
                                      style={"bottomMargin": "20"})),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            dcc.Input(
                                id="input-text", type="text", value="Enter Video ID"
                            )
                        ),
                        html.Br(),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        html.Div(
                            dcc.Checklist(
                                id="types",
                                options=[
                                    {"label": "Toxicity", "value": "Toxicity"},
                                    {"label": "Insult", "value": "Insult"},
                                    {"label": "Obscenity", "value": "Obscenity"},
                                    {"label": "Prejudice", "value": "Prejudice"},
                                ],
                                values=["Toxicity"],
                            )
                        )
                    ],
                    className="two columns",
                ),
            ],
            className="row",
            style={"marginBottom": "20"},
        ),
        html.Div([html.Button("Submit", id="button", className="button-primary")], className="eleven columns"),
    ]
)
