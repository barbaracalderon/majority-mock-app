import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_mantine_components as dmc


def merge_data():
    bills_df = pd.read_csv("data/bills.csv")
    legislators_df = pd.read_csv("data/legislators.csv")
    votes_df = pd.read_csv("data/votes.csv")
    vote_results_df = pd.read_csv("data/vote_results.csv")

    vote_results_merged = pd.merge(
        vote_results_df,
        legislators_df,
        left_on="legislator_id",
        right_on="id",
        suffixes=("_vote", "_legislator"),
    )

    vote_results_merged = pd.merge(
        vote_results_merged,
        votes_df,
        left_on="vote_id",
        right_on="id",
        suffixes=("_vote_results", "_votes"),
    )

    vote_results = pd.merge(
        vote_results_merged,
        bills_df,
        left_on="bill_id",
        right_on="id",
        suffixes=("_votes", "_bills"),
    )

    final_table = pd.merge(
        vote_results,
        legislators_df[["id", "name"]],
        left_on="sponsor_id",
        right_on="id",
        how="left",
    )

    final_table.drop(columns=["id_vote", "id_votes", "id_bills"], inplace=True)
    print(final_table)
    return final_table


def clean_data(data):
    bill_data = data.drop(
        columns=[
            "id",
            "legislator_id",
            "vote_id",
            "id_legislator",
            "bill_id",
            "sponsor_id",
        ]
    ).rename(
        columns={
            "name_x": "legislator",
            "name_y": "primary sponsor",
            "vote_type": "position",
        }
    )

    bill_data["position"] = bill_data["position"].replace({1: "Yea", 2: "Nay"})
    print(bill_data)
    return bill_data


data = merge_data()
bill_data = clean_data(data)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(
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


@callback(
    Output("tabs-navbar-content", "children"),
    Input("tabs-navbar", "value"),
)
def render_content(tab):
    if tab == "tab-about":
        return html.Div(
            children=[
                html.H4("What we do"),
                html.Div(
                    children=[
                        html.P(
                            children="Majority is the indispensable tool for public affairs professionals seeking to maximize their impact in today's dynamic political environment. Our innovative software platform empowers users to streamline their workflow, from mapping out strategies to tracking progress and driving meaningful change. With Majority, you can stay ahead of the curve, anticipate shifts in the policy landscape, and leverage actionable insights to drive success. Experience the power of Majority and elevate your public affairs game today."
                        ),
                        html.Hr(),
                        html.P(
                            children="To provide a glimpse into the capabilities of our tools, we offer two additional tabs: 'Bills' and 'Legislators', each serving as a comprehensive resource for public affairs professionals."
                        ),
                        html.Br(),
                        html.P(
                            children="In the 'Bills' tab, gain insights into legislative dynamics by uncovering critical information such as the number of legislators who supported and opposed each bill. Discover the primary sponsor behind each bill, shedding light on key influencers shaping policy decisions. Meanwhile, in the 'Legislators' tab, delve into the voting behavior of individual legislators. Explore how many bills each legislator has supported or opposed, gaining valuable insights into their legislative track record and stance on various issues."
                        ),
                        html.Br(),
                        html.P(
                            children="With these powerful features at your fingertips, our tools offer unparalleled insights and empower you to navigate the complexities of public affairs with precision and confidence."
                        ),
                        html.P(children="Let information reach you."),
                        html.Hr(),
                        html.P(
                            children=[
                                html.Em(
                                    "PS: This is a mock application for a technical challenge. The name 'Majority' was an inspiration used in order not to mention the official company name. Developed by Barbara Calderon."
                                )
                            ]
                        ),
                    ]
                ),
            ]
        )
    elif tab == "tab-bills":
        return html.Div(
            children=[
                html.H4("Bills"),
                html.P(
                    "Please, select which bill would you like to see more information on."
                ),
                dcc.Dropdown(
                    id="bill-dropdown",
                    options=[
                        {"label": title, "value": title}
                        for title in data["title"].unique()
                    ],
                    searchable=False,
                    clearable=False,
                    placeholder="Select the bill",
                ),
                html.Br(),
                html.P(id="bill-sponsor"),
                html.Br(),
                html.Div(
                    children=[
                        dmc.Container(
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        [
                                            dash_table.DataTable(
                                                id="bill-table",
                                                data=[],
                                                page_size=12,
                                                style_table={"overflowX": "auto"},
                                            )
                                        ],
                                        span=5,
                                    ),
                                    dmc.Col([dcc.Graph(id="bill-graph")], span=6),
                                ]
                            )
                        ),
                    ]
                ),
            ]
        )
    elif tab == "tab-legislators":
        return html.Div(
            children=[
                html.H4("Legislators"),
                html.P(
                    "Please, select the legislator whose votes you would like to see more information on."
                ),
                dcc.Dropdown(
                    id="legislator-dropdown",
                    options=[
                        {"label": legislator, "value": legislator}
                        for legislator in bill_data["legislator"].unique()
                    ],
                    searchable=False,
                    clearable=False,
                    placeholder="Select the Legislator",
                ),
                html.Br(),
                html.P(id="legislator-votes"),
                html.Br(),
                html.Div(
                    children=[
                        dmc.Container(
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        [
                                            dash_table.DataTable(
                                                id="legislator-table",
                                                data=[],
                                                page_size=14,
                                                style_table={"overflowX": "auto"},
                                            )
                                        ],
                                        span=6,
                                    ),
                                    dmc.Col([dcc.Graph(id="legislator-graph")], span=5),
                                ]
                            )
                        ),
                    ]
                ),
            ]
        )


@callback(Output("bill-table", "data"), Input("bill-dropdown", "value"))
def update_table(value):
    bill_filtered_data = bill_data[bill_data["title"] == value]
    bill_filtered_data = bill_filtered_data.drop(columns=["title", "primary sponsor"])
    return bill_filtered_data.to_dict("records")
