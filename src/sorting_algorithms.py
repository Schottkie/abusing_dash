import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

length = 10
x_values = list(range(0, length))
y_values = numpy.random.randint(1000, size=length)

fig = go.Figure(data=[
    go.Bar(x=x_values, y=y_values, marker={'color': 'crimson'})
])
app.layout = html.Div([
    html.P(),
    html.H2('Race of the sorting algorithms'),
    html.Div([
        html.H5('Bubble sort'),
        html.Div([
            html.Div([
                html.P('Number of iterations: ')
            ], className='six columns'),
            html.Div([
                html.P(0, id='num_of_iter')
            ], className='two columns'),
        ], className='four columns'),
        html.Div([
            html.Div([
                html.P('Number to sort: ')
            ], className='six columns'),
            html.Div([
                html.P(y_values[0], id='sorted_value'),
            ], className='two columns'),
        ], className='four columns'),
        html.Div([
            html.Div([
                html.P('Index to sort: ')
            ], className='six columns'),
            html.Div([
                html.Div(0, id='index'),
            ], className='two columns'),
        ], className='four columns'),
        html.Div([
            html.Div([
                html.P('Index already sorted: ')
            ], className='six columns'),
            html.Div([
                html.Div(0, id='index_sorted'),
            ], className='two columns'),
        ], className='four columns'),
    ], className='elven columns'),
    html.Div([
        dcc.Graph(id='graph', figure=fig, config={'displayModeBar': False}),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        ),
    ], className='elven columns'),
    html.Div([
        html.H5('Quick sort')
    ], className='elven columns'),
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
    app.run_server(debug=True)
