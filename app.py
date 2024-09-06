from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import polars as pl
import components as cmp
from utils import get_top_entries

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pl.read_csv("data/all_data.csv")
city_df = pl.read_csv("data/city-data.csv")
state_df = pl.read_csv("data/state-data.csv")

location_options = {'city': 'By City', 'state': 'By State'}
location_type_tabs = cmp.create_tabs(id="location-type-tabs", options=location_options)

cities = df['city'].unique().sort()
city_options = {city: city for city in cities}
city_select = cmp.create_select(id="city-select", options=city_options)

states = df['state'].unique().sort()
state_options = {state: state for state in states}
state_select = cmp.create_select(id="state-select", options=state_options)

fig_container_style = {'height': '50vh'}
map_fig_container = dcc.Graph(id="map-fig", style=fig_container_style)
city_bar_fig_container = dcc.Graph(id="city-bar-fig", style=fig_container_style)
state_bar_fig_container = dcc.Graph(id="state-bar-fig", style=fig_container_style)

footer = cmp.create_footer()

app.layout = html.Div([
    dbc.Container([
        # Header section
        dbc.Row([
            dbc.Col([
                html.H1("Top Wikipedia People Pages by Location U.S. (2015-2019)", className='text-center', style={'color': cmp.PRIMARY_COLOR})
            ], md=8, sm=12, className='my-2'),
            dbc.Col([
                html.P("Explore the Most Visited Wikipedia Pages for Each City and Town Across the U.S. from 2015 to 2019", className='lead')
            ], md=4, sm=12, className='my-2')
        ], className='my-2'),
        
        # Map chart
        dbc.Row([
            dbc.Col([
                location_type_tabs
            ], width=12, className='my-2'),
            dbc.Col([
                map_fig_container
            ], width=12, className='my-2')
        ], className='mb-4'),

        # City and State charts
        dbc.Row([
            dbc.Col([
                    dbc.Col([
                        city_select
                    ], width=12, className='my-2'),
                    dbc.Col([
                        city_bar_fig_container
                    ], width=12, className='my-2')
            ], lg=6, md=12, className='mb-4'),
            dbc.Col([
                    dbc.Col([
                        state_select
                    ], width=12, className='my-2'),
                    dbc.Col([
                        state_bar_fig_container
                    ], width=12, className='my-2')
            ], lg=6, md=12, className='mb-4')
        ], className='mb-4')
    ],
    fluid=True,
    className='mx-auto'),
    html.Div([html.Br()], style={'backgroundColor': cmp.BACKGROUND_COLOR}),

    # Footer section
    footer
], style={'backgroundColor': cmp.BACKGROUND_COLOR})


@app.callback(
    Output("map-fig", "figure"),
    [Input("location-type-tabs", "active_tab")]
)
def update_map(location_type):
    if not location_type or location_type == 'city':
        return cmp.create_map_fig(city_df, 'city', 'total_views_sum')
    elif location_type == 'state':
        return cmp.create_map_fig(state_df, 'state', 'total_views_sum')

@app.callback(
    Output("city-bar-fig", "figure"),
    [Input("city-select", "value")]
)
def update_city_bar_fig(city):
    if not city:
        city = 'Los Angeles'
    filtered_df = get_top_entries(df, 'city', city)
    fig = cmp.create_bar_fig(filtered_df, 'name', 'views_sum', city)
    
    return fig

@app.callback(
    Output("state-bar-fig", "figure"),
    [Input("state-select", "value")]
)
def update_state_bar_fig(state):
    if not state:
        state = 'California'
    filtered_df = get_top_entries(df, 'state', state)
    fig = cmp.create_bar_fig(filtered_df, 'name', 'views_sum', state)
    
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)