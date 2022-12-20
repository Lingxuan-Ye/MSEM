from sys import argv

import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from source import Query

app = Dash(__name__)

port = '8050' if len(argv) == 1 else argv[1]

colors = {'background': '#111111', 'foreground': '#777777','text': '#7FDBFF'}

query = Query()

# I would say, most of the style property are not working,
# and that I used to hate XML-like syntax most but this is
# even more torturing. I would rather write pure HTML and CSS.
app.layout = html.Div(
    [
        html.Div(
            [
                html.Br(),
                html.H1(
                    'IE6600 Team Project',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Br(),
                html.H3(
                    'We would be grateful if anyone comes up with '
                    'a better introduction.',
                    style={'textAlign': 'center', 'color': colors['text']}
                ),

                html.Br(),
                dcc.Graph(id='map-selected'),

                html.Br(),
                html.Div(
                    [
                        html.Label(
                            'Select Map',
                            style={
                            'padding': 5,
                            'backgroundColor': colors['foreground'],
                            'color': colors['text']
                        }
                        ),
                        dcc.Dropdown(
                            options=query.available,
                            value='population',
                            id='map-label'
                        )
                    ],
                    style={'padding': 10, 'flex': 1}
                )
            ],
            style={'backgroundColor': colors['background']}
        ),
        html.Br(),
        html.Div(
            [
                html.Br(),
                html.Details(
                    [
                        html.Summary(
                            'Click to find more...',
                            style={'color': colors['text']}
                        ),
                        html.Iframe(
                            src='//player.bilibili.com/player.html?aid=80433022&bvid=BV1GJ411x7h7&cid=137649199&page=1',
                            style={
                                'scrolling': 'no',
                                'border': '0',
                                'frameborder': 'no',
                                'framespacing': '0',
                                'allowfullscreen': 'true'
                            }
                        )
                    ]
                )
            ],
            style={'padding': 10, 'flex': 1}
        )
    ]
)


@app.callback(Output('map-selected', 'figure'), Input('map-label', 'value'))
def switch(map_label: str):
    return go.Figure(
        go.Choroplethmapbox(
            geojson=query.geojson,
            locations=query.fips,
            z=getattr(query, map_label),
            colorscale='Viridis',
            zauto=True,
            marker_opacity=0.5,
            marker_line_width=0,
        ),
        layout=go.Layout(
            mapbox_style='open-street-map',
            mapbox_zoom=3,
            mapbox_center={'lat': 37.0902, 'lon': -95.7129},
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
    )


if __name__ == '__main__':
    app.run(port=port, debug=False)
