
# coding: utf-8

# In[ ]:

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("/Users/Benjamin/Documents/nama_10_gdp_1_Data.csv")

available_indicators = df["UNIT"].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.H1('Gross domestic product at market prices for the EU',style={'text-align':'center','font-family':'monospace'}),
    html.Div([
        html.H2(children='GDP by indicator (scatter plot)',style={'text-align':'center','font-family':'monospace'}),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Current prices, million euro"
            ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Chain linked volumes, index 2010=100"
            ),
            
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df["TIME"].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df["TIME"].unique()}
    ),
    html.Div([
        html.H2(children='GDP by indicator and country(line chart)',style={'margin-top':'5%','text-align':'center','font-family':'monospace'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='indicator-select',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Current prices, million euro'
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='country-select',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    value="European Union (28 countries)"
                ),
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),
        dcc.Graph(id='indicator-graphicline'),
    ])
    ])
    
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                year_value):
    dff = df[df["TIME"] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff["UNIT"] == xaxis_column_name]['Value'],
            y=dff[dff["UNIT"] == yaxis_column_name]['Value'],
            text=dff[dff["UNIT"] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 20,
                'opacity': 0.40,
                'line': {'width': 0.6, 'color': 'blue'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
               },
            yaxis={
                'title': yaxis_column_name,
                },
            margin={'l': 80, 'b': 40, 't': 20, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphicline', 'figure'),
    [dash.dependencies.Input('indicator-select', 'value'),
     dash.dependencies.Input('country-select', 'value'),])
def update_graph(indicator_name, country_name):
    dff = df[df['GEO'] == country_name]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['UNIT'] == indicator_name]['TIME'],
            y=dff[dff['UNIT'] == indicator_name]['Value'],
            text=dff[dff['UNIT'] == indicator_name]['Value'],
            mode='lines',
            line = dict(
                color = ('green'),
                width = 4,)
        )],
        'layout': go.Layout(
            xaxis={
                'title': country_name,
            },
            yaxis={
                'title': indicator_name,
            },
            margin={'l': 80, 'b': 40, 't': 20, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

