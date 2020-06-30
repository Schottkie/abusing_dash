import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


external_stylesheets = ['./assets/stlesheet.css', './assets/bootstrap.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

length = 10
x_values = list(range(0, length))
y_values = numpy.random.randint(1000, size=length)

fig = go.Figure(data=[
    go.Bar(x=x_values, y=y_values, marker={'color': 'crimson'})
])
app.layout = html.Div([
    html.H2('Sorting algorithms'),
    dbc.Card([
        dbc.CardHeader(html.H5('Bubble sort'), style={'textAlign': 'center'}),
        dbc.CardBody(html.Div([
            dcc.Graph(id='graph', figure=fig, config={'displayModeBar': False}),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            ),
        ])),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.P('Number of iterations: ')),
                        dbc.Col(html.P(0, id='num_of_iter'))
                    ])
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.P('Number to sort: ')),
                        dbc.Col(html.P(y_values[0], id='sorted_value'))
                    ])
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.P('Index to sort: ')),
                        dbc.Col(html.Div(0, id='index')),
                    ])
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.P('Index already sorted: ')),
                        dbc.Col(html.Div(0, id='index_sorted')),
                    ])
                ]),
            ])
        ])
    ], outline=True, color='red')
])

@app.callback([Output('num_of_iter', 'children'),
               Output('graph', 'figure'),
               Output('sorted_value', 'children'),
               Output('index', 'children'),
               Output('index_sorted', 'children')],
              [Input('interval-component', 'n_intervals')],
              [State('graph', 'figure'),
               State('index', 'children'),
               State('num_of_iter', 'children'),
               State('index_sorted', 'children')])
def update_metrics(_, graph_figure, index_children, num_of_iter_children, index_sorted_children):
    if index_sorted_children == 1:
        return num_of_iter_children, graph_figure, graph_figure['data'][0]['y'][
            index_children], index_children, index_sorted_children
    if len(graph_figure['data'][0]['y']) == index_children+1 or (index_sorted_children == index_children+1 and index_children != 0):
        index_sorted_children = index_children
        index_children = 0
        num_of_iter_children = num_of_iter_children + 1
    elif graph_figure['data'][0]['y'][index_children] > graph_figure['data'][0]['y'][index_children+1]:
        graph_figure['data'][0]['y'][index_children], graph_figure['data'][0]['y'][index_children+1] = graph_figure['data'][0]['y'][index_children+1], graph_figure['data'][0]['y'][index_children]
        index_children = index_children + 1
        num_of_iter_children = num_of_iter_children + 1
    else:
        index_children = index_children + 1
        num_of_iter_children = num_of_iter_children + 1

    colors = ['crimson'] * len(graph_figure['data'][0]['y'])
    colors[index_children] = '#a2f274'
    if index_sorted_children != 0:
        for elem in range(index_sorted_children, len(graph_figure['data'][0]['y'])):
            colors[elem] = '#e6e6e6'
    graph_figure['data'][0]['marker']['color'] = colors
    return num_of_iter_children, graph_figure, graph_figure['data'][0]['y'][index_children], index_children, index_sorted_children

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
