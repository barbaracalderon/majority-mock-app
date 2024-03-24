from dash import Dash, dcc, html, Input, Output, callback, dash_table
from data import bill_data

@callback(Output("bill-table", "data"), Input("bill-dropdown", "value"))
def update_table(value):
    bill_filtered_data = bill_data[bill_data["title"] == value]
    bill_filtered_data = bill_filtered_data.drop(columns=["title", "primary sponsor"])
    return bill_filtered_data.to_dict("records")

@callback(Output("legislator-table", "data"), Input("legislator-dropdown", "value"))
def update_table(value):
    legislator_filtered_data = bill_data[bill_data["legislator"] == value]
    legislator_filtered_data = legislator_filtered_data.drop(
        columns=["legislator", "primary sponsor"]
    )
    return legislator_filtered_data.to_dict("records")