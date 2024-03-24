from dash import Dash, dcc, html
from callback_functions import render_content, show_sponsor, update_table, update_graph


def create_app():
    external_stylesheets: list[str] = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app: Dash = Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True,
    )

    app.layout = html.Div(
        style={"margin": "auto", "fontFamily": "Arial, sans-serif", "width": "50%"},
        children=[
            html.Div(
                children=[
                    html.H1(children="Majority"),
                    html.H5(
                        children="We provide insights into the voting behaviour of US legislators on various bills."
                    ),
                ]
            ),
            html.Br(),
            dcc.Tabs(
                id="tabs-navbar",
                value="tab-about",
                children=[
                    dcc.Tab(label="About us", value="tab-about"),
                    dcc.Tab(label="Bills", value="tab-bills"),
                    dcc.Tab(label="Legislators", value="tab-legislators"),
                ],
            ),
            html.Div(id="tabs-navbar-content"),
        ],
    )
    return app
