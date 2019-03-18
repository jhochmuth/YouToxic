import dash_core_components as dcc
import dash_html_components as html


text_layout = html.Div([
    html.Div([
        html.H2('YouToxic – Text Analysis',
                style={'color': 'rgb(200, 200, 200)'}),
        html.Img(src='assets/image-2.png')],
        style={'fontFamily': 'arial black', 'marginBottom': '20'},
        className='banner'),
    html.Details([
        html.Summary('Click here to view instructions.', style={'color': 'rgb(0,0,0'}),
        html.Div('– Enter text that you wish to analyze.'),
        html.Div('– Select types of toxicity to analyze text for.', style={'marginBottom': '10'})
    ],
        style={'color': 'rgb(175, 175, 175', 'marginBottom': '20'}
    ),
    html.Div(id='text-container', style={'marginBottom': '20'}),
    dcc.Input(id='input-text', type='text', value='Enter Text', size=100, style={'marginBottom': '10'}),
    dcc.Checklist(
        id='types',
        options=[
            {'label': 'Toxicity', 'value': 'toxic'},
            {'label': 'Insult', 'value': 'insult'},
            {'label': 'Obscenity', 'value': 'obscene'},
            {'label': 'Prejudice', 'value': 'prejudice'}
        ],
        values=['toxic'],
        style={'marginBottom': '10'}
    ),
    html.Div([
        html.Button('Submit', id='button')
    ], className='twelve columns')
])