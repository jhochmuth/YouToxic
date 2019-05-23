"""Defines page layout for analysis of tweets.

"""
import datetime

import dash_core_components as dcc

import dash_html_components as html


tweet_layout = html.Div(
    [
        html.Div(
            html.Details(
                [
                    html.Summary(
                        "Click here to view instructions.", style={"color": "rgb(0,0,0"}
                    ),
                    html.Div(
                        "– Enter Twitter username, maximum number of tweets to analyze."
                    ),
                    html.Div("– Select types of toxicity to analyze tweets for."),
                    html.Div(
                        '– To select a date range, click "Limit by Date" option and make selections.'
                    ),
                    html.Div(
                        '– If option "All Tweets" is selected, tweets analyzed will be the most recent.'
                    ),
                    html.Div(
                        "– Due to limitations of Twitter, the maximum number of tweets to analyze is 3240.",
                    ),
                ],
                style={"color": "rgb(125, 125, 125", "marginTop": 20},
            ), className="row",
        ),
        dcc.Loading(id="loading-1",
                    type="cube",
                    color="#00CC00",
                    children=html.Div(id="tweet-container",
                                      style={"marginTop": 20, "marginBottom": 20})),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            dcc.Input(
                                id="input-text", type="text", value="Enter Username"
                            ),
                            style={"marginBottom": 10}
                        ),
                        html.Div(
                            dcc.Input(id="input-num", type="number", value=10),
                        ),
                    ],
                    className="two columns",
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
                html.Div(
                    [
                        html.Div(
                            dcc.RadioItems(
                                id="limit-by-date",
                                options=[
                                    {"label": "All Tweets", "value": "all"},
                                    {"label": "Limit by Date", "value": "date"},
                                ],
                                value="all",
                                labelStyle={"display": "inline-block"},
                                inputStyle={"margin-left": "20px"},
                            )
                        ),
                        html.Div(
                            [
                                dcc.DatePickerRange(
                                    id="date-picker",
                                    minimum_nights=0,
                                    initial_visible_month=datetime.date.today(),
                                )
                            ]
                        ),
                    ],
                    className="two columns",
                ),
            ],
            className="row",
            style={"marginBottom": 20},
        ),
        html.Div([html.Button("Submit", id="button", className="button-primary")], className="row"),
    ]
)
