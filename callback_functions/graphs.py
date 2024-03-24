from data import bill_data
from dash import Dash, dcc, html, Input, Output, callback, dash_table

@callback(Output("bill-graph", "figure"), Input("bill-dropdown", "value"))
def update_graph(value):
    bill_filtered_data = bill_data[bill_data["title"] == value]
    x_values = bill_filtered_data["position"].unique()
    y_values = [
        bill_filtered_data[bill_filtered_data["position"] == x_val].shape[0]
        for x_val in x_values
    ]

    fig = {
        "data": [{"type": "bar", "x": x_values, "y": y_values, "name": "Count"}],
        "layout": {
            "title": "Number of votes for the selected bill",
            "xaxis": {"title": "Position taken"},
            "yaxis": {"title": "Number of votes"},
        },
    }
    return fig

@callback(Output("legislator-graph", "figure"), Input("legislator-dropdown", "value"))
def update_graph(value):
    legislator_filtered_data = bill_data[bill_data["legislator"] == value]
    x_values = legislator_filtered_data["position"].unique()
    y_values = [
        legislator_filtered_data[legislator_filtered_data["position"] == x_val].shape[0]
        for x_val in x_values
    ]

    fig = {
        "data": [{"type": "bar", "x": x_values, "y": y_values, "name": "Count"}],
        "layout": {
            "title": "Overall position in bills",
            "xaxis": {"title": "Position taken"},
            "yaxis": {"title": "Number of bills"},
        },
    }
    return fig