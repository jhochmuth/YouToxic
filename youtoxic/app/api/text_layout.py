"""Defines page layout for analysis of text entered manually.

"""
import dash_core_components as dcc

import dash_html_components as html


text_layout = html.Div(
    [
        html.Div(id="text-container", style={"marginBottom": "20"}),
        html.Details(
            [
                html.Summary(
                    "Click here to view instructions.", style={"color": "rgb(0,0,0"}
                ),
                html.Div("– Enter text that you wish to analyze."),
                html.Div(
                    "– Select types of toxicity to analyze text for.",
                    style={"marginBottom": "10"},
                ),
            ],
            style={"color": "rgb(175, 175, 175", "marginBottom": "20"},
        ),
        dcc.Input(
            id="input-text",
            type="text",
            value="Enter Text",
            size=100,
            style={"marginBottom": "10"},
        ),
        dcc.Checklist(
            id="types",
            options=[
                {"label": "Toxicity", "value": "toxic"},
                {"label": "Insult", "value": "insult"},
                {"label": "Obscenity", "value": "obscene"},
                {"label": "Prejudice", "value": "prejudice"},
            ],
            values=["toxic"],
            style={"marginBottom": "10"},
        ),
        html.Div([html.Button("Submit", id="button", className="button-primary")], className="twelve columns"),
    ]
)
