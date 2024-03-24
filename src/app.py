from dash import Dash, dcc, html, Input, Output, callback
from callback_functions import (
    render_content,
    show_bill_sponsor,
    show_legislator_sponsor,
    update_bill_table,
    update_legislator_table,
    update_bill_graph,
    update_legislator_graph,
)


external_stylesheets: list[str] = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

server = app.server

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

app.callback(Output("tabs-navbar-content", "children"), Input("tabs-navbar", "value"))(
    render_content
)
app.callback(Output("bill-sponsor", "children"), Input("bill-dropdown", "value"))(
    show_bill_sponsor
)
app.callback(
    Output("legislator-votes", "children"), Input("legislator-dropdown", "value")
)(show_legislator_sponsor)
app.callback(Output("bill-table", "data"), Input("bill-dropdown", "value"))(
    update_bill_table
)
app.callback(Output("legislator-table", "data"), Input("legislator-dropdown", "value"))(
    update_legislator_table
)
app.callback(Output("bill-graph", "figure"), Input("bill-dropdown", "value"))(
    update_bill_graph
)
app.callback(
    Output("legislator-graph", "figure"), Input("legislator-dropdown", "value")
)(update_legislator_graph)
