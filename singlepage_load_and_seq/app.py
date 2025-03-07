# dash template for combined wastewate viral load and clinical count tracking
# From Msomi and Levy et al. 2025

from dash import html, dcc, Dash, Input, Output, callback # now including callbacks
import dash_bootstrap_components as dbc
import pandas as pd 
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.express.colors import qualitative
from datetime import timedelta

# load case and viral load data
def load_rsa_cases_and_levels():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/rsa_cases_vs_levels.feather")

# Now get the sequencing data outputs
def load_monthly_data():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/NICD_monthly.feather")

def load_monthly_data_smoothed():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/NICD_daily_smoothed.feather")

# choose start and end dates 
start_date = '2024-06-01'
end_date =  '2024-12-01'

# alternatively, the current date can be used. 
# end = date.today()

df = load_rsa_cases_and_levels()

# use a preset styling, here we use LUX. 
app = Dash(external_stylesheets = [dbc.themes.LUX])

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

#The callback allows figures to be updated based on user input - This is what makes the dashboard interactive.
@callback(
    Output("seq_graph0", "figure"),
    Input("plottype", "value"))
def seq_plot(plottype):
    colorMap = qualitative.Light24
    names = {'variable':'Lineage', 'index':'Month', 'value':'Prevalence'}
    if plottype=='monthly':
        seq_df = load_monthly_data()
        seq_df = seq_df[seq_df.index >=start_date]
        seq_df = seq_df[seq_df.index <=end_date]
        seq_df = seq_df[seq_df.sum(axis=1)>0]
        fig2 = go.Figure(data=[go.Bar(name=sfc, x=seq_df.index, y=seq_df[sfc], marker_color=colorMap[j]) for j, sfc in enumerate(seq_df.columns)])
        
        # set bar mode to stack and configure to desired format
        fig2.update_layout(barmode='stack',yaxis_tickformat = '.0%')
        fig2.update_layout(legend_title_text=names['variable'])
        fig2.update_xaxes(title_text="",hoverformat = "%b %Y")
        fig2.update_layout(xaxis_range=[pd.to_datetime(start_date)-timedelta(days=15), pd.to_datetime(end_date)+timedelta(days=15)], template='none')
    else:
        seq_df_daily  = load_monthly_data_smoothed()
        seq_df_daily = seq_df_daily[seq_df_daily.index >=start_date]

        fig2 = go.Figure([go.Scatter(name=sfc,x=seq_df_daily.index, y=seq_df_daily[sfc], marker_color=colorMap[j],
                                      mode='lines', stackgroup='one', fillcolor=colorMap[j],
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

# describe what the page layout should look like
app.layout = html.Div([
    html.H1(id="H1", children="SARS-CoV-2 Wastewater-integrated Surveillance",
            style={'color': 'black',"textAlign": "center"}),
    html.Hr(),
    html.P('A bit of information about the wastewater monitoring program.',
           style={'color': 'black',"textAlign": "center"}),
    dcc.Graph(figure=bar_chart(), id='test-graph', config={'displayModeBar': False}),
    html.P('Some information on wastewater sequencing. ',
           style={'color': 'black',"textAlign": "center"}),
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
    dbc.Row(
    dcc.Graph(id="seq_graph0", config={'displayModeBar': False}),
    style={"width": "100%", "align-items": "center", 'justify-content': 'center', 'margin': 'auto'}
    )
    ])

if __name__ == "__main__":
    #run server, debug option is used to see errors in the web app. 
    app.run_server(debug=False)

