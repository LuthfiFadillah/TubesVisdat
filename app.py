import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
# first you have to load the geojson file
import json
import numpy as np
from ast import literal_eval
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
mapbox_access_token = 'pk.eyJ1IjoidGlmYWhudXJyIiwiYSI6ImNqdmFtcjNlNzBlZHE0ZWw5eG94bHF1aG8ifQ.jqDIvTaqJKnNaI7Gqogvow'

def get_color_for_val(val, vmin, vmax, pl_colorscale):
    if vmin >= vmax:
        raise ValueError('vmin should be < vmax')
        
    plotly_scale, plotly_colors = list(map(float, np.array(pl_colorscale)[:,0])), np.array(pl_colorscale)[:,1]  
    colors_01=np.array(list(map(literal_eval,[color[3:] for color in plotly_colors] )))/255.#color codes in [0,1]
    
    v= (val - vmin) / float((vmax - vmin)) #here val is mapped to v in[0,1]
    #find two consecutive values in plotly_scale such that   v belongs to the corresponding interval
    idx = 0
   
    while(v > plotly_scale[idx+1]): 
        idx+=1
    left_scale_val = plotly_scale[idx]
    right_scale_val = plotly_scale[idx+ 1]
    vv = (v - left_scale_val) / (right_scale_val - left_scale_val)##attn! this code works well if the plotly_scale is 
                                                              #sorted ascending, and there are no duplicates in
                                                              # plotly_scale
    #get the  [0,1]-valued color code representing the rgb color corresponding to val
    val_color01 = colors_01[idx]+vv*(colors_01[idx + 1]-colors_01[idx])
    val_color_0255 = list(map(np.uint8, 255*val_color01+0.5))
    return 'rgb'+str(tuple(val_color_0255))


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_def = pd.read_csv(
    'deforestation.csv')

with open("idn_map.json") as geofile:
    geoJSON = json.load(geofile)

sources=[]
for feat in geoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})

df_map=pd.read_csv('idn_deforest.csv')
lons=[]
lats=[]
for k in range(len(geoJSON['features'])):
    county_coords=np.array(geoJSON['features'][k]['geometry']['coordinates'][0])
    
    lontotal = 0
    lattotal = 0
    for l in county_coords:
        l = np.array(l)
        if (isinstance(l[0], np.ndarray)):
            m, M = l[:,0].min(), l[:,0].max()
            lontotal = lontotal + (0.5*(m+M))
            m, M = l[:,1].min(), l[:,1].max()
            lattotal = lattotal + (0.5*(m+M))
        else:
            j = l
            lontotal = lontotal + j[0]
            lattotal = lattotal + j[1]
    lons.append(lontotal / len(county_coords))
    lats.append(lattotal / len(county_coords))

app.layout = html.Div([
    html.Div([
        html.Div([
        dcc.Graph(id="my-graph")
        ], className="map", style = {"width": "60%"}),
        html.Div([
        dcc.Slider(
        id='my-slider',
        min=2001,
        max=2018,
        step=1,
        value=2018,
        marks={
            2001 : '2001',
            2005 : '2005',
            2010 : '2010',
            2015 : '2015',
            2018 : '2018'
        }
        )
        ],className="row", style={"width":"56%", "textAlign":"center", "padding-left":"6%", "padding-bottom":"30px"}),
    ]),
    html.Div([
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
        )], style={'columnCount' :1, 'padding-top': '5%'}),
        html.Div([
            dcc.RadioItems(
                    id='select-chart',
                    options=[
                    {'label': 'Biomass Loss', 'value': 'Biomass Loss'},
                    {'label': 'CO2 Emissions', 'value': 'CO2 Emissions'}
                    ],
                    value='Biomass Loss',
                    labelStyle={'display': 'inline-block'}
                )
            ],style={'width': '600px', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='time-series')
        ],style={'width': '70%', 'float': 'left'}),
        html.Div(id="slideshow-container", children=[
            html.Div(id="content"),
            dcc.Interval(id="interval", interval=3000),
            #dcc.Markdown('''## In **2018**, the top 5 regions responsible for **55.85%** Indonesia's Tree Cover Loss'''),
            #dcc.Markdown('''* 1. Kalimantan Timur   184.517 ha'''),
            #dcc.Markdown('''* 2. Kalimantan Barat   159.429 ha'''),
            #dcc.Markdown('''* 3. Sumatera Selatan   125.584'''),
            #dcc.Markdown('''* 4. Kalimantan Tengah   110.423 ha'''),
            #dcc.Markdown('''* 5. Riau   101.210 ha'''),
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
], className="container")


@app.callback(
    Output("my-graph", "figure"),
    [Input("my-slider", "value")]
)
def update_figure(selected):

    def title(text):
        return text

    deforest = df_map[str(selected)]
    pl_colorscale= [[0.0, 'rgb(246, 233, 195)'],
                [0.1, 'rgb(235, 210, 123)'], 
                [0.4, 'rgb(185, 148, 83)'],
                [0.7, 'rgb(137, 112, 34)'],
                [1.0, 'rgb(82, 67, 24)']] 
    facecolor=[get_color_for_val(d, min(deforest), max(deforest), pl_colorscale)  for d in deforest] 

    prop=[geoJSON['features'][k]['properties']['Propinsi'] for k in range(len(geoJSON['features']))]

    text=[c+' '+'{:0.2f}'.format(r)+'Ha' for c, r in zip(prop, deforest)]

    Idn = dict(type='scattermapbox',
                 lat=lats, 
                 lon=lons,
                 text=text,
                 mode='markers',
                 marker=dict(size=1, color=facecolor),
                 showlegend=False,
                 hoverinfo='text',
                )

    title = "Deforestation in Indonesia Year " + str(selected)
    layers=[dict(
    			sourcetype = 'geojson',
                 source = sources[k],
                 below = 'water',
                 type = 'fill',   
                 color =facecolor[k],
                 opacity=0.8
                ) for k in range(len(sources))]



    layout = dict(font=dict(family='Balto'),
                  autosize=False,
                  width=900,
                  height=450,
                  hovermode='closest',
       
				  title=title,
                  mapbox=dict(accesstoken=mapbox_access_token,
                              layers=layers,
                              bearing=0,
                              center=dict(
                              lat=-2.6, 
                              lon=118),
                              pitch=0,
                              zoom=3.5,
                        ) 
                  )



    # fig = dict(data=[Idn], layout=layout)
    return {
        "data": [Idn],
        "layout": layout

    }

@app.callback(
    Output('time-series', 'figure'),
    [Input('select-province', 'value'),
    Input('select-chart', 'value')]
)
def update_figure(selected_province, selected_chart):
    filtered_df = df_def[df_def.province == selected_province]
    traces = []
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
    if selected_chart=='Biomass Loss':
        traces.append(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['biomass'],
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
            },
        yaxis='y2'
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
        yaxis='y2'
        ))
    print(traces)
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Year'},
            yaxis={'title': 'Tree Cover Loss'},
            yaxis2={'title': selected_chart,
            		'overlaying': 'y',
            		'side': 'right'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

@app.callback(Output('content', 'children'),
              [Input('interval', 'n_intervals')])
def display_image(n):
    if n == None or n % 3 == 1:
        content = html.Div([
            dcc.Markdown('''## In **2018**, the top 5 regions responsible for **55.85%** Indonesia's Tree Cover Loss'''),
            dcc.Markdown('''* 1. Kalimantan Timur   184.517 ha'''),
            dcc.Markdown('''* 2. Kalimantan Barat   159.429 ha'''),
            dcc.Markdown('''* 3. Sumatera Selatan   125.584'''),
            dcc.Markdown('''* 4. Kalimantan Tengah   110.423 ha'''),
            dcc.Markdown('''* 5. Riau   101.210 ha'''),
            ])
    elif n % 3 == 2:
        content = html.Div([
            dcc.Markdown('''## In **2018**, the top 5 regions responsible for **52.86%** Indonesia's Biomass Loss'''),
            dcc.Markdown('''* 1. Kalimantan Timur   47,45 Mt'''),
            dcc.Markdown('''* 2. Kalimantan Barat   31,69 Mt'''),
            dcc.Markdown('''* 3. Kalimantan Tengah   22,91 Mt'''),
            dcc.Markdown('''* 4. Sumatera Selatan   18,39 Mt'''),
            dcc.Markdown('''* 5. Riau   17,97 Mt'''),
            ])
    elif n % 3 == 0:
        content = html.Div([
            dcc.Markdown('''## In **2018**, the top 5 regions responsible for **52.87%** Indonesia's CO2 Emissions'''),
            dcc.Markdown('''* 1. Kalimantan Timur   86,99 Mt'''),
            dcc.Markdown('''* 2. Kalimantan Barat   58,1 Mt'''),
            dcc.Markdown('''* 3. Kalimantan Tengah   42 Mt'''),
            dcc.Markdown('''* 4. Sumatera Selatan   33,72 Mt'''),
            dcc.Markdown('''* 5. Riau   32,94 Mt''')
            ])
    else:
        content = "None"
    return content

server = app.server # the Flask app

if __name__ == '__main__':
    app.run_server(debug=True)