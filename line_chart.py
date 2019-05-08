import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from dash.dependencies import Input, Output

import plotly.graph_objs as go

df = pd.read_csv(
    'deforestation.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Label('Select Province'),
        dcc.Dropdown(
            id='select-province',
            options=[
                {'label': 'Indonesia', 'value': 'Indonesia'},
                {'label': 'Aceh', 'value': 'Aceh'},
                {'label': 'Bali', 'value': 'Bali'},
                {'label': 'Bangka Belitung', 'value': 'Bangka Belitung'},
                {'label': 'Banten', 'value': 'Banten'},
                {'label': 'Bengkulu', 'value': 'Bengkulu'},
                {'label': 'Gorontalo', 'value': 'Gorontalo'},
                {'label': 'Jakarta Raya', 'value': 'Jakarta Raya'},
                {'label': 'Jambi', 'value': 'Jambi'},
                {'label': 'Jawa Barat', 'value': 'Jawa Barat'},
                {'label': 'Jawa Tengah', 'value': 'Jawa Tengah'},
                {'label': 'Jawa Timur', 'value': 'Jawa Timur'},
                {'label': 'Kalimantan Barat', 'value': 'Kalimantan Barat'},
                {'label': 'Kalimantan Selatan', 'value': 'Kalimantan Selatan'},
                {'label': 'Kalimantan Tengah', 'value': 'Kalimantan Tengah'},
                {'label': 'Kalimantan Timur', 'value': 'Kalimantan Timur'},
                {'label': 'Kepulauan Riau', 'value': 'Kepulauan Riau'},
                {'label': 'Lampung', 'value': 'Lampung'},
                {'label': 'Maluku', 'value': 'Maluku'},
                {'label': 'Maluku Utara', 'value': 'Maluku Utara'},
                {'label': 'Nusa Tenggara Barat', 'value': 'Nusa Tenggara Barat'},
                {'label': 'Nusa Tenggara Timur', 'value': 'Nusa Tenggara Timur'},
                {'label': 'Papua', 'value': 'Papua'},
                {'label': 'Papua Barat', 'value':'Papua Barat'},
                {'label': 'Riau', 'value': 'Riau'},
                {'label': 'Sulawesi Barat', 'value': 'Sulawesi Barat'},
                {'label': 'Sulawesi Selatan', 'value': 'Sulawesi Selatan'},
                {'label': 'Sulawesi Tengah', 'value': 'Sulawesi Tengah'},
                {'label': 'Sulawesi Tenggara', 'value': 'Sulawesi Tenggara'},
                {'label': 'Sulawesi Utara', 'value': 'Sulawesi Utara'},
                {'label': 'Sumatera Barat', 'value': 'Sumatera Barat'},
                {'label': 'Sumatera Selatan', 'value': 'Sumatera Selatan'},
                {'label': 'Sumatera Utara', 'value': 'Sumatera Utara'},
                {'label': 'Yogyakarta', 'value': 'Yogyakarta'}
            ],
            value='Aceh', style={'width': '200px'}
    )], style={'columnCount' :1}),
    html.Div([
        dcc.RadioItems(
                id='select-chart',
                options=[
                {'label': 'Tree Cover Loss', 'value': 'Tree Cover Loss'},
                {'label': 'Biomass Loss', 'value': 'Biomass Loss'},
                {'label': 'CO2 Emissions', 'value': 'CO2 Emissions'}
                ],
                value='Tree Cover Loss',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '600px', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='time-series')
    ],style={'width': '70%', 'float': 'left'}),
    html.Div([
        dcc.Markdown('''## In **2018**, the top 5 regions responsible for **55.85%** Indonesia's Tree Cover Loss'''),
        dcc.Markdown('''* 1. Kalimantan Timur   184.517 ha'''),
        dcc.Markdown('''* 2. Kalimantan Barat   159.429 ha'''),
        dcc.Markdown('''* 3. Sumatera Selatan   125.584'''),
        dcc.Markdown('''* 4. Kalimantan Tengah   110.423 ha'''),
        dcc.Markdown('''* 5. Riau   101.210 ha'''),
        #dcc.Markdown('''## In **2018**, the top 5 regions responsible for **52.86%** Indonesia's Biomass Loss'''),
        #dcc.Markdown('''* 1. Kalimantan Timur   47,45 Mt'''),
        #dcc.Markdown('''* 2. Kalimantan Barat   31,69 Mt'''),
        #dcc.Markdown('''* 3. Kalimantan Tengah   22,91 Mt'''),
        #dcc.Markdown('''* 4. Sumatera Selatan   18,39 Mt'''),
        #dcc.Markdown('''* 5. Riau   17,97 Mt'''),
        #dcc.Markdown('''## In **2018**, the top 5 regions responsible for **52.87%** Indonesia's CO2 Emissions'''),
        #dcc.Markdown('''* 1. Kalimantan Timur   86,99 Mt'''),
        #dcc.Markdown('''* 2. Kalimantan Barat   58,1 Mt'''),
        #dcc.Markdown('''* 3. Kalimantan Tengah   42 Mt'''),
        #dcc.Markdown('''* 4. Sumatera Selatan   33,72 Mt'''),
        #dcc.Markdown('''* 5. Riau   32,94 Mt''')
    ],style={'width': '30%', 'float': 'right'})
])


@app.callback(
    Output('time-series', 'figure'),
    [Input('select-province', 'value'),
    Input('select-chart', 'value')]
    )
def update_figure(selected_province, selected_chart):
    filtered_df = df[df.province == selected_province]
    traces = []
    if selected_chart == 'Tree Cover Loss':
        traces.append(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['tc'],
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
            },
        ))
    elif selected_chart=='Biomass Loss':
        traces.append(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['biomass'],
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
            },
        ))
    else:
        traces.append(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['co2'],
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
            },
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Year'},
            yaxis={'title': selected_chart},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)