import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
# first you have to load the geojson file
import json
import numpy as np
from ast import literal_eval

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


app = dash.Dash(__name__)


with open("idn_map.json") as geofile:
    geoJSON = json.load(geofile)

# lons=[]
# lats=[]
# for k in range(len(geoJSON['features'])):
#     county_coords=np.array(geoJSON['features'][k]['geometry']['coordinates'][1])
#     county_coords=np.array(county_coords[0])
#     print(county_coords)
#     m, M =county_coords[:,0].min(), county_coords[:,0].max()
#     lons.append(0.5*(m+M))
#     m, M =county_coords[:,1].min(), county_coords[:,1].max()
#     lats.append(0.5*(m+M))

# print(lons)
# print(lats)
sources=[]
for feat in geoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})

df=pd.read_csv('idn_deforest.csv')
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

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id="my-graph")
    ], className="map", style = {"width": "70%"}),
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
    ],className="row", style={"width":"70%", "textAlign":"center", "padding-left":"6%"}),
    

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("my-slider", "value")]
)
def update_figure(selected):

    def title(text):
        return text

    deforest = df[str(selected)]
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
                 hoverinfo='text'
                )

    layers=[dict(sourcetype = 'geojson',
                 source = sources[k],
                 below = 'water',
                 type = 'fill',   
                 color =facecolor[k],
                 opacity=0.8
                ) for k in range(len(sources))]



    layout = dict(title=selected,
                  font=dict(family='Balto'),
                  autosize=False,
                  width=1100,
                  height=600,
                  hovermode='closest',
       
                  mapbox=dict(accesstoken=mapbox_access_token,
                              layers=layers,
                              bearing=0,
                              center=dict(
                              lat=-2.6, 
                              lon=118),
                              pitch=0,
                              zoom=3.8,
                        ) 
                  )



    # fig = dict(data=[Idn], layout=layout)
    return {
        "data": [Idn],
        "layout": layout

    }


server = app.server # the Flask app

if __name__ == '__main__':
    app.run_server(debug=True)