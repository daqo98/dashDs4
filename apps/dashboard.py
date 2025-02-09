import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pathlib
from app import app
import dash_bootstrap_components as dbc
# colombian map dependencies
from utils import mapcolombia
from utils import plot_by_year
import pandas as pd


base_final = pd.read_csv('https://storage.googleapis.com/ds4all-test-bd1/base_final.csv')

figmap, dpts_count, colombia = mapcolombia.getfigmap(base_final)
fig_years_dist = plot_by_year.ploting_distribution()

controlsMap = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label('year'),
                dcc.Dropdown(
                    id='year',
                    options=[{'value': i, 'label': i} for i in dpts_count['anno_encuesta_x'].unique()],
                    value=dpts_count['anno_encuesta_x'].unique()[0]
                ),
            ]
        )
    ],
    body=True,
)

card_map = dbc.Card(
    dbc.CardBody([    
        html.H4("Colombian map by years"),
        html.Div(controlsMap),
        html.Div(
            dcc.Graph(
                id='colombia_plot',
                figure=figmap
            )
        )     
    ])
)

card_graph_distribution = dbc.Card([
    dbc.CardBody([
        dcc.Graph(
            id='years_dist_plot',
            figure=fig_years_dist
        )
    ])
])


layout = html.Div([
    dbc.Row([
        dbc.Col(
            card_map, width = 6
        )
    ]
    ),
    dbc.Row([
        dbc.Col(
            card_graph_distribution, width = 12
        )
      ]
    )
])


@app.callback(
    Output('colombia_plot', 'figure'),
    Input('year', 'value'),
)
def graph_map_per_year(year=2018):
    dpts_count_filtered = dpts_count[dpts_count['anno_encuesta_x'] == year]
    figmap = px.choropleth_mapbox(dpts_count_filtered, geojson=colombia, locations='nom_dpto',
                                  featureidkey="properties.DPTO_CNMBR",
                                  color='count_ratio',
                                  color_continuous_scale='ylorrd',
                                  mapbox_style="carto-positron",
                                  zoom=3, center={"lat": 4.570868, "lon": -74.297333},
                                  opacity=0.5,
                                  labels={'unemp': 'unemployment rate'}
                                  )
    figmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return figmap