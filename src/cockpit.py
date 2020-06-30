import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
import flask
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

external_stylesheets = ['./assets/stlesheet.css', './assets/bootstrap.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
)
application = app.server

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=0,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Speed", 'font': {'size': 24}},
    number= {'suffix': "km/h"},
    gauge={
        'axis': {'range': [0, 250], 'showticksuffix': 'last', 'ticksuffix': 'km/h', 'tickwidth': 1, 'tickcolor': "darkblue", 'tick0': 0, 'dtick': 10},
        'bar': {'color': "yellow"},
        'bgcolor': "black",
        'borderwidth': 2,
        'bordercolor': "yellow",
        'steps': [
            {'range': [0, 30], 'color': 'black'},
            {'range': [30, 33], 'color': 'orange'},
            {'range': [33, 50], 'color': 'black'},
            {'range': [50, 55], 'color': 'orange'},
            {'range': [55, 250], 'color': 'black'},
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 240}}))

fig.update_layout(paper_bgcolor="black", font={
                  'color': "yellow", 'family': "Arial"})

graphs = make_subplots(
    rows=2, cols=2,
    specs=[
        [{'colspan': 2}, None],
        [{}, {}],
    ],
    subplot_titles=("Distance", "Speed", "Acceleration"),
)
graphs.add_trace(
    go.Scatter(x=[0],
               y=[0],
               line=dict(color='yellow')),
    row=1, col=1)
graphs.add_trace(
    go.Scatter(x=[0],
               y=[0],
               line=dict(color='yellow')),
    row=2, col=1)
graphs.add_trace(
    go.Scatter(x=[0],
               y=[0],
               line=dict(color='yellow')),
    row=2, col=2)
graphs.update_layout(
    showlegend=False, template='plotly_dark', font={'color': 'yellow'},
    paper_bgcolor='black', xaxis={'ticksuffix': 's'},
    yaxis={'ticksuffix': 'm'},
    xaxis2={'ticksuffix': 's'},
    yaxis2={'ticksuffix': 'm/s'},
    xaxis3={'ticksuffix': 's'},
    yaxis3={'ticksuffix': 'm/s²'})

app.layout = html.Div(
    [dcc.Graph(
        figure=fig, id='tachometer', config={'displayModeBar': False}),
     dbc.Row(
         [dbc.Col(
             html.Button(
                 'Break', id='break', n_clicks_timestamp=0,
                 style={'minWidth': '100%', 'minHeight': '50px',
                        'backgroundColor': 'black',
                        'border': '2px solid yellow', 'color': 'yellow'}),),
          dbc.Col(
              html.Button(
                  'Gas', id='gas', n_clicks_timestamp=0,
                  style={'minWidth': '100%', 'minHeight': '50px',
                         'backgroundColor': 'black',
                         'border': '2px solid yellow', 'color': 'yellow'}))
        ], style={'minWidth': '100%', 'minHeight': '50px',
                'backgroundColor': 'black', 'margin': '0'}),
     dcc.Interval(
         id='tact', interval=1 * 1000, n_intervals=0, disabled=True,),
     html.Div(
         style={'minWidth': '100%', 'minHeight': '50px',
                'backgroundColor': 'black'}),
     dcc.Graph(
         figure=graphs, id='stats', config={'displayModeBar': False})])

@app.callback(
    [Output('tachometer', 'figure'),
     Output('tact', 'disabled'),
     Output('stats', 'figure')],
    [Input('gas', 'n_clicks_timestamp'),
     Input('break', 'n_clicks_timestamp'),
     Input('tact', 'n_intervals')],
    [State('tachometer', 'figure'),
     State('stats', 'figure')]
)
def accelarate(gas_n_timestamp, break_n_timestamp, _, tachometer_figure,
               stats_figure):
    if gas_n_timestamp == 0 and break_n_timestamp == 0:
        return tachometer_figure, True, stats_figure

    # 1m/s²
    acceleration = 1
    if gas_n_timestamp > break_n_timestamp and tachometer_figure['data'][0][
            'gauge']['threshold']['value'] > tachometer_figure['data'][0][
            'value'] + (acceleration * 12960) * (1 / 3600):

        # speed
        stats_figure['data'][1]['y'].append(
            tachometer_figure['data'][0]['value'] / 3.6)
        stats_figure['data'][1]['x'].append(len(stats_figure['data'][1]['x']))

        # distance
        stats_figure['data'][0]['y'].append(
            np.trapz(stats_figure['data'][1]['y']))
        stats_figure['data'][0]['x'].append(len(stats_figure['data'][1]['x']))

        # acceleration a=1
        stats_figure['data'][2]['y'].append(acceleration)
        stats_figure['data'][2]['x'].append(len(stats_figure['data'][1]['x']))

        #v_tach_new = v_tach_old + a * dt
        tachometer_figure['data'][0]['value'] = tachometer_figure['data'][0]['value'] + (
            acceleration * 12960) * (1/3600)
        trigger = False
    elif gas_n_timestamp > break_n_timestamp:
        stats_figure['data'][1]['y'].append(
            tachometer_figure['data'][0]['gauge']['threshold']['value'] / 3.6)
        stats_figure['data'][1]['x'].append(len(stats_figure['data'][1]['x']))
        stats_figure['data'][0]['y'].append(
            np.trapz(stats_figure['data'][1]['y']))
        stats_figure['data'][0]['x'].append(len(stats_figure['data'][1]['x']))
        stats_figure['data'][2]['y'].append(0)
        stats_figure['data'][2]['x'].append(len(stats_figure['data'][1]['x']))
        tachometer_figure['data'][0]['value'] = tachometer_figure['data'][0]['gauge']['threshold']['value']
        trigger = False
    elif gas_n_timestamp < break_n_timestamp and \
            (tachometer_figure['data'][0]['value'] - (acceleration * 12960) * (1/3600)) > 0:
        # speed
        stats_figure['data'][1]['y'].append(
            tachometer_figure['data'][0]['value'] / 3.6)
        stats_figure['data'][1]['x'].append(len(stats_figure['data'][1]['x']))

        # distance
        stats_figure['data'][0]['y'].append(
            np.trapz(stats_figure['data'][1]['y']))
        stats_figure['data'][0]['x'].append(len(stats_figure['data'][1]['x']))

        # acceleration a=-1
        stats_figure['data'][2]['y'].append(-acceleration)
        stats_figure['data'][2]['x'].append(len(stats_figure['data'][1]['x']))

        #v_tach_new = v_tach_old + a * dt
        tachometer_figure['data'][0]['value'] = tachometer_figure['data'][0]['value'] - (
            acceleration * 12960) * (1/3600)
        trigger = False
    else:
        stats_figure['data'][1]['y'].append(0)
        stats_figure['data'][1]['x'].append(len(stats_figure['data'][1]['x']))
        stats_figure['data'][0]['y'].append(
            np.trapz(stats_figure['data'][1]['y']))
        stats_figure['data'][0]['x'].append(len(stats_figure['data'][1]['x']))
        stats_figure['data'][2]['y'].append(0)
        stats_figure['data'][2]['x'].append(len(stats_figure['data'][1]['x']))
        tachometer_figure['data'][0]['value'] = 0
        trigger = True

    return tachometer_figure, trigger, stats_figure

if __name__ == '__main__':
    application.run(debug=True)
