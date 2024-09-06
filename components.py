from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from utils import format_metric

BACKGROUND_COLOR = '#F0F4F8'
ALTERNATIVE_BACKGROUND_COLOR = '#E1E6F0'
PRIMARY_COLOR = '#5C6F84'
PRIMARY_COLOR_RGBA = 'rgba(92, 111, 132, 0.8)'
SECONDARY_COLOR = '#B4A6A1'

def create_tabs(id, options):
    tabs = dbc.Tabs(
        id=id,
        children=[
            dbc.Tab(
                label=label, 
                tab_id=value,
                tab_style={'background-color': ALTERNATIVE_BACKGROUND_COLOR},
                label_style={'color': SECONDARY_COLOR, 'font-size': '18px', 'font-weight': '500'},
                active_label_style={'color': 'white', 'background-color': PRIMARY_COLOR}
            ) 
            for value, label in options.items()
        ]
    )
    return tabs

def create_select(id, options):
    formatted_options = [
        {'label': label, 'value': value} 
        for value, label in options.items()
        if label is not None and value is not None
    ]
    dropdown = dcc.Dropdown(
        id=id,
        options=formatted_options,
        style={'color': PRIMARY_COLOR},
        className='mb-2',
        clearable=True,
        searchable=True
    )
    return dropdown

def create_map_fig(df, location, metric):
    custom_colorscale = [
        [0, '#5c6f84'],
        [0.1, '#578fac'],
        [0.2, '#41b1cc'],
        [0.3, '#11d4e2'],
        [0.4, '#5af0e6'],
        [1, '#03f7eb']
    ]

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lng",
        color=metric,
        text="name",
        hover_name="name",
        custom_data=[location, metric],
        color_continuous_scale=custom_colorscale,
        zoom=3,
    )

    fig.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=ALTERNATIVE_BACKGROUND_COLOR,
        autosize=True,
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title=format_metric(metric),
            title_font=dict(size=14, color=PRIMARY_COLOR),
            tickfont=dict(size=12, color=PRIMARY_COLOR),
        )
    )

    hovertemplate = (
        "<b>%{text}</b><br>"
        "Location: %{customdata[0]}<br>"
        "Total Views: %{customdata[1]:,.0f}<br>"
        "<extra></extra>"
    )

    fig.update_traces(
        textfont=dict(
            color='rgba(0, 0, 0, 0.8)',
            size=12,
            weight=500
        ),
        hovertemplate=hovertemplate
    )

    if location == 'city':
        fig.update_traces(marker=dict(size=10))
    if location == 'state':
        fig.update_traces(marker=dict(size=30))

    return fig

def create_bar_fig(df, x, y, location):
    fig = px.bar(
        df,
        x=y,
        y=x,
        title=f"Top Wikipedia Pages with Most {format_metric(y)} in {location}",
        text=y,
        labels={y: format_metric(x)},
        color_discrete_sequence=[PRIMARY_COLOR],
        orientation='h'
    )

    fig.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=ALTERNATIVE_BACKGROUND_COLOR,
        margin={"r":0,"t":30,"l":0,"b":0},
        title=dict(
            font=dict(
                size=20,
                color=PRIMARY_COLOR
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=format_metric(y),
        yaxis_title='',
        font=dict(
            size=12,
            color=PRIMARY_COLOR
        ),
    )

    fig.update_traces(
        textfont=dict(
            size=12,
            color=PRIMARY_COLOR,
            weight=700
        ),
        textposition='outside',
        texttemplate='%{text:,.0f}'
    )

    max_y_value = df[y].max()
    fig.update_xaxes(range=[0, max_y_value * 1.2])

    return fig

def create_footer():
    link_style = {
    'color': PRIMARY_COLOR,
    'font-weight': 'bold',
    'font-size': '16px',
    'text-decoration': 'none'
    }
    footer = html.Footer(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            "Source Code",
                            href="https://github.com/Alfredomg7/wikipedia-people-dashboard",
                            target="_blank",
                            style=link_style
                        ),
                        className='text-center'
                    ),
                    dbc.Col(
                        html.A(
                            "Data Source",
                            href="https://github.com/the-pudding/data/tree/master/people-map",
                            target="_blank",
                            style=link_style
                        ),
                        className='text-center'
                    ),
                ],
                className='justify-content-center',
            )
        ],
        className='py-3',
        style={
            'background-color': BACKGROUND_COLOR,
            'position': 'fixed',
            'bottom': '0',
            'width': '100%',
            'box-shadow': f"0px 0px 8px {PRIMARY_COLOR_RGBA}",
            'z-index': '1000'
        }
    )
    return footer

                    