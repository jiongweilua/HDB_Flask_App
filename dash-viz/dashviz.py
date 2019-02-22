import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./combined_data_2017_newfeatures.csv')
df['hoverinfo'] = [list(a) for a in  zip(df.corrected_address, df.resale_price)]


mapbox_access_token = 'pk.eyJ1Ijoiamlvbmd3ZWlsdWEiLCJhIjoiY2pzZzR1djB6MWt5eDN5bG43bWpueGNkNCJ9.m3kYxGJOvWdokivqHNAaXQ'


colors = {
    'text': '#3b5998'
}

app.layout = html.Div(
    children = [

    html.H1(
        children='Map of Resale Flats in Singapore',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='mapviz',
        figure={
            'data': [
                go.Scattermapbox(
                    lat=df[df['flat_type'] == i]['lat'],
                    lon=df[df['flat_type'] == i]['lon'],
                    text=df[df['flat_type'] == i]['hoverinfo'],
                    opacity=0.7,
                    marker={
                        'size': 4,
                    },
                    name=i
                ) for i in df.flat_type.unique()
            ],
            'layout': go.Layout(
                autosize = True,
                hovermode='closest',
                height = 1000,
                width = 1400,
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=1.3526, 
                        lon=103.8352),
                    pitch = 0,
                    zoom = 11)
            )
        }
    ),

    html.H3('Filter Towns for Plots Below',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    dcc.Dropdown(
        id='my-dropdown',
        options = [{'label': str(x) , 'value': str(x)} for x in df.town.unique()],
        value = ['ANG MO KIO','HOUGANG','TAMPINES'],
        multi=True),

    dcc.Graph(id='price-vs-centrality'),

    dcc.Graph(id='price-vs-mrt'),

    
])

@app.callback(
    dash.dependencies.Output('price-vs-mrt','figure'),
    [dash.dependencies.Input('my-dropdown','value')])
def update_figure(selected_towns):
    print(selected_towns)
    if type(selected_towns) is str:
        filtered_df = df[df['town'].isin([selected_towns])]
    else:
        filtered_df = df[df['town'].isin(selected_towns)]

    return { 
    'data': [go.Scatter(
                    x=filtered_df[filtered_df['town'] == i]['Distance to Nearest MRT'],
                    y=filtered_df[filtered_df['town'] == i]['resale_price'],
                    text=filtered_df[filtered_df['town'] == i]['flat_type'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in filtered_df.town.unique()],
    'layout': go.Layout(
                xaxis={'title': 'Distance to Nearest MRT'},
                yaxis={'type':'log', 'title': 'Resale Price'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )

    }


@app.callback(
    dash.dependencies.Output('price-vs-centrality','figure'),
    [dash.dependencies.Input('my-dropdown','value')])
def update_figure(selected_towns):
    print(selected_towns)
    if  type(selected_towns) is str:
        filtered_df = df[df['town'].isin([selected_towns])]
    else:
        filtered_df = df[df['town'].isin(selected_towns)]

    return { 
    'data': [go.Scatter(
                    x=filtered_df[filtered_df['town'] == i]['Distance to City Centre'],
                    y=filtered_df[filtered_df['town'] == i]['resale_price'],
                    text=filtered_df[filtered_df['town'] == i]['flat_type'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in filtered_df.town.unique()],
    'layout': go.Layout(
                xaxis={'title': 'Distance to City Centre'},
                yaxis={'type':'log', 'title': 'Resale Price'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )

    }


if __name__ == '__main__':
    app.run_server(debug=True)