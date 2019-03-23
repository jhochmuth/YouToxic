"""For predicting the toxicity of manually-entered text."""

import dash_html_components as html

import dash_table

import pandas as pd


def get_text_predictions(text, types, pipeline):
    """Returns the toxicity predictions for the entered text.

    Parameters
    ----------
    text: str
        The text to predict.

    types: List
        The types of toxicity to predict for.

    pipeline: Object
        The pipeline object used to make predictions.

    Returns
    -------
        The html layout for the subsection of the page that contains the results.

    """
    if not text:
        return html.Div('Error: You must enter some text.',
                        style={'color': 'rgb(255, 0, 0'})

    if not types:
        return html.Div('Error: You must select at least one type of toxicity.',
                        style={'color': 'rgb(255, 0, 0'})

    types_order, preds, judgements = list(), dict(), dict()

    if 'toxic' in types:
        preds['Toxicity'], judgements['Toxicity'] = pipeline.predict_toxicity(text)
        types_order.append('Toxicity')
    if 'insult' in types:
        preds['Insult'], judgements['Insult'] = pipeline.predict_insult(text)
        types_order.append('Insult')
    if 'obscene' in types:
        preds['Obscenity'], judgements['Obscenity'] = pipeline.predict_obscenity(text)
        types_order.append('Obscenity')
    if 'prejudice' in types:
        preds['Prejudice'], judgements['Prejudice'] = pipeline.predict_prejudice(text)
        types_order.append('Prejudice')

    df = pd.DataFrame()
    df['type'] = types_order
    df['judgement'] = df['type'].map(judgements)
    df['pred'] = df['type'].map(preds)
    df['pred'] = df['pred'].map('{:.3f}'.format)

    table = dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'Analysis Type', 'id': 'type'},
            {'name': 'Judgement', 'id': 'judgement'},
            {'name': 'Prediction', 'id': 'pred'}
        ],
        data=df.to_dict('rows'),
        style_table={'border': 'thin black solid'},
        style_header={'fontWeight': 'bold',
                      'backgroundColor': 'rgb(220,220,220)',
                      'textAlign': 'center'},
        style_cell={'textAlign': 'left',
                    'fontFamily': 'optima',
                    'border': 'thin lightgrey solid',
                    'padding': 10},
        style_data={'whiteSpace': 'normal'},
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
    )

    return html.Div([
        html.P('Text analyzed: {}'.format(text), style={'marginBottom': '10'}),
        table
    ])
