import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from datetime import timedelta
from load_data import load_monthly_data, load_monthly_data_smoothed, load_rsa_cases_and_levels, load_color_map
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/seq')

start_date = '2024-06-01'
end_date =  '2024-12-01'

def new_container():
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H1(id="H1", children="SARS-CoV-2 Wastewater Surveillance", style={'color': 'white'}),
                width=12
            ),
            style={"textAlign": "center", "paddingTop": 30, "paddingBottom": 30, "backgroundColor": "#A6CE39"}
        ),
        html.Div(style={'height': '15px'}),
        html.P(
            id="seq_intro",
            children=['Basic info on wastewater sequencing analyses'],
            style={"font-size": 20,"textAlign": "center"}
        ),
        html.Div(style={'height': '30px'}),
        html.H3(
            id="H3", children="SARS-CoV-2 Lineage Prevalence Observed via Wastewater",
            style={"textAlign": "center", "marginTop": 5, "marginBottom": 5}
        ),
        html.Div(style={'height': '15px'}),
        html.Div(
            dbc.RadioItems(
                id="plottype",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "Monthly Trends", "value": "monthly"},
                    {"label": "Smoothed Daily Trends", "value": "daily"}
                ],
                value="daily",
                style={"width": "100%", "justify-content": "flex-end"}
            ),
            style={"marginTop": 0, "marginBottom": 0}
        ),
        html.Div(style={'height': '15px'}),
        dbc.Row(
            dcc.Graph(id="seq_graph0", config={'displayModeBar': False}),
            style={"width": "100%", "align-items": "center", 'justify-content': 'center', 'margin': 'auto'}
        )
    ], fluid=True)

layout = new_container

@callback(
    Output("seq_graph0", "figure"),
    Input("plottype", "value"))
def seq_plot(plottype):
    colorMap = load_color_map()
    names = {'variable':'Lineage', 'index':'Month', 'value':'Prevalence'}
    if plottype=='monthly':
        seq_df = load_monthly_data()
        seq_df = seq_df[seq_df.index >=start_date]
        seq_df = seq_df[seq_df.index <=end_date]
        seq_df = seq_df[seq_df.sum(axis=1)>0]
        fig2 = go.Figure(data=[go.Bar(name=sfc, x=seq_df.index, y=seq_df[sfc], marker_color=colorMap[sfc]) for j, sfc in enumerate(seq_df.columns)])
        
        # set bar mode to stack and configure to desired format
        fig2.update_layout(barmode='stack',yaxis_tickformat = '.0%')
        fig2.update_layout(legend_title_text=names['variable'])
        fig2.update_xaxes(title_text="",hoverformat = "%b %Y")
        fig2.update_layout(xaxis_range=[pd.to_datetime(start_date)-timedelta(days=15), pd.to_datetime(end_date)+timedelta(days=15)], template='none')
    else:
        seq_df_daily  = load_monthly_data_smoothed()
        seq_df_daily = seq_df_daily[seq_df_daily.index >=start_date]

        fig2 = go.Figure([go.Scatter(name=sfc,x=seq_df_daily.index, y=seq_df_daily[sfc], marker_color=colorMap[sfc],
                                      mode='lines', stackgroup='one', fillcolor=colorMap[sfc],
                                      line=dict(width=0.0)) for j, sfc in enumerate(seq_df_daily.columns)])
        fig2.update_layout(legend_title_text=names['variable'],hovermode='x unified',hoverlabel=dict(font_size=12), yaxis_tickformat = '.0%')
        fig2.update_layout(xaxis_range=[start_date, end_date], template='none')
        fig2.update_xaxes(title_text="",hoverformat = "%b %d %Y")
    fig2.update_layout(
        legend=dict(
        orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
        font={'size':15}
    ),margin=dict(l=40, r=75, t=15, b=0))

    fig2.update_yaxes(title_text="Lineage Prevalence",
                      range=[0,1.01],
                      automargin=True,
                      title_standoff=20
    )
    return fig2
