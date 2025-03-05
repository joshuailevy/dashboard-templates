from dash import html
import dash_bootstrap_components as dbc


def create_navbar():

    navbar = dbc.Navbar(
        id="navbar",
        children=[
                    dbc.Col(html.A([
                        html.H1('LOGO-HERE'),
                    ],href="/"),width={'size':3,'offset':1}),
                    dbc.Col(
                        dbc.DropdownMenu(
                            nav=True,
                            in_navbar=True,
                            label="Menu",
                            align_end=True,
                            children=[  # Add as many menu items as you need
                                dbc.DropdownMenuItem("SARS-CoV-2- Levels", href='/',style = {'font-size':16}),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem("SARS-CoV-2- Variants", href='/seq',style = {'font-size':16}),
                            ],
                        style={"float":'left','font-size':24}),
                    width={'size':3,'offset':6}),
        ],
        #sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="white",
        dark=False,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar


def create_footer():
    FOOTER_STYLE = {
        "bottom": 0,
        "left": 0,
        "right": 0,
        "text-align": "center",
        "height": "10rem",
        "padding": "1rem 1rem",
        "background-color": "white",
    }
    fdivs = [html.Hr(),
             html.P(children='Custom footer, to be included on all pages.',
             style={"font-weight": "bold",'color':'black'})
             ]
    footer = html.Div(fdivs, style=FOOTER_STYLE)
    return footer