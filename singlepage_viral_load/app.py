# dash template for combined wastewate viral load and clinical count tracking
# From Msomi and Levy et al. 2025

from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import pandas as pd 
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# load case and viral load data
def load_rsa_cases_and_levels():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/rsa_cases_vs_levels.feather")

# choose start and end dates 
start_date = '2024-10-04'
end_date =  '2025-03-01'

# alternatively, the current date can be used. 
# end = date.today()

df = load_rsa_cases_and_levels()

# use a preset styling, here we use MINTY. 
app = Dash(external_stylesheets = [dbc.themes.MINTY])

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
        secondary_y=False)

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
            secondary_y=True)

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

#describe what the page layout should look like
app.layout = html.Div([
    html.H1(id="H1", children="SARS-CoV-2 Wastewater-integrated Surveillance",
            style={'color': 'black',"textAlign": "center"}),
    html.Hr(),
    html.P('A bit of information about the wastewater monitoring program.',
           style={'color': 'black',"textAlign": "center"}),
    dcc.Graph(figure=bar_chart(), id='test-graph', config={'displayModeBar': False})
    ])

if __name__ == "__main__":
    #run server, debug option is used to see errors in the web app. 
    app.run_server(debug=False)

