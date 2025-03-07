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

dash.register_page(__name__, path='/')

start_date = '2024-06-01'
end_date =  '2024-12-01'

#Creating a function to for a bar chart to compare the wastewater levels to the clinical cases
def bar_chart():
    df = load_rsa_cases_and_levels()
    # in our data, end is the end of the epiweek
    df['end'] = pd.to_datetime(df['end'])
    df = df[df['end']>=start_date]
    df = df[df['end']<=end_date]
    
    df_s = df[['end','sum_genomes']]
    df_s = df_s[~df_s['sum_genomes'].isna()]
    # calculate a simple rolling average.
    df_s['ww_smoothed'] =df_s['sum_genomes'].rolling(window=5,min_periods=0,center=True).mean()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df['end'], y=df['n'],
            marker_color='lightgray',
            name="Clinical",
            hovertemplate='%{y} cases',
            textposition = "none"),
        secondary_y=False) #This will plot the clinical cases on the primary (left) y-axis

    fig.add_trace(
        go.Scatter(
            x=df['end'], y=df['sum_genomes'],
            mode='markers',
            line=dict(color="cornflowerblue", width=4),
            hovertemplate='%{y} copies/mL',
            name="Wastewater"),
            secondary_y=True)

    fig.add_trace(
        go.Scatter(
            x=df_s['end'], y=df_s['ww_smoothed'],
            mode='lines',
            line=dict(color="cornflowerblue", width=4),
            hovertemplate='%{y} copies/mL',
            name="Smoothed wastewater"),
            secondary_y=True) #The wastewater levels will be plotted on the secondary y-axis (right)

    fig.update_layout(
        template='none',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
    margin=dict(l=45, r=0, t=20, b=50))
    fig.update_xaxes(hoverformat = "%Y, Epiweek %W",)
    fig.update_yaxes(title_text="Laboratory confirmed cases",
                     secondary_y=False,
                     range=[0,df['n'].max()*1.02],
                     showgrid=False,
                     automargin=True,
                     title_standoff=20  # Add space between y-axis label and graph
                     )
    fig.update_yaxes(title_text="Genome Copies/ml (N Gene)",
                     secondary_y=True,
                     range=[0,df['sum_genomes'].max()*1.02],
                     automargin=True,
                     title_standoff=20  # Add space between y-axis label and graph
                     )
    fig.update_traces(hoverinfo = 'name+y',cliponaxis=False)
    return fig


#Function to specify the layout of the page including the title, intro paragraph and positioning of graphs 
def home_container():
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
            id="intro",
            children=(
                'Basic info about virus levels in wastewater...'
            ),
            style={"font-size": 20,"textAlign": "center"}
        ),
        html.Div(style={'height': '25px'}),
        html.H3(
            id="H3_", children='National SARS-CoV-2 Wastewater Levels',
            style={"textAlign": "center", "marginTop": 10, "marginBottom": 0}
        ),
        html.Div(style={'height': '15px'}),
        dbc.Row(
            dcc.Graph(id="bar_plot", figure=bar_chart(), config={'displayModeBar': False,'doubleClick': 'reset'}),
            style={"width": "100%", "align-items": "center", 'justify-content': 'center', 'margin': 'auto'}
        )
    ], fluid=True)

layout = home_container



