import dash_core_components as dcc
import dash_html_components as html


file_layout = html.Div([
    html.Div([
        html.H2('YouToxic – Text Analysis',
                style={'color': 'rgb(200, 200, 200)'}),
        html.Img(src='assets/image-2.png')],
        style={'fontFamily': 'arial black', 'marginBottom': '20'},
        className='banner'),
    html.Details([
        html.Summary('Click here to view instructions.', style={'color': 'rgb(0,0,0'}),
        html.Div('– Select types of toxicity to analyze texts in file for.'),
        html.Div('– Upload a file.'),
        html.Div('– File must be in csv or xls format.'),
        html.Div('– File must contain a column named "text" (case sensitive), which contains texts to analyze.',
                 style={'marginBottom': '10'})
    ],
        style={'color': 'rgb(175, 175, 175', 'marginBottom': '20'}
    ),
    html.Div(id='file-container', style={'marginBottom': '10'}),
    html.Div([
        dcc.Checklist(
            id='types',
            options=[
                {'label': 'Toxicity', 'value': 'Toxicity'},
                {'label': 'Insult', 'value': 'Insult'},
                {'label': 'Obscenity', 'value': 'Obscenity'},
                {'label': 'Prejudice', 'value': 'Prejudice'}
            ],
            values=['Toxicity']
        )
    ],
        id='submit-field',
        style={'marginBottom': '10'}
    ),
    html.Div(
        dcc.Upload(
            id='upload-data',
            children='Drag and drop or click to manually select file',
            style={
                'width': '95%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
    ),
    html.Br(),
])
