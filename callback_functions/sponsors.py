from dash import Input, Output, callback
from data import bill_data
from typing import Any


def show_bill_sponsor(value: Any) -> str:
    bill_filtered_data = bill_data[bill_data["title"] == value]
    primary_sponsor = ""
    if not bill_filtered_data.empty:
        primary_sponsors = bill_filtered_data["primary sponsor"]
        if not primary_sponsors.isnull().all():
            primary_sponsor = primary_sponsors.dropna().iloc[0]
    return f"Primary sponsor: {primary_sponsor}"


def show_legislator_sponsor(value: Any) -> str:
    legislator_filtered_data = bill_data[bill_data["legislator"] == value]
    legislator_name = ""
    if not legislator_filtered_data.empty:
        legislator_names = legislator_filtered_data["legislator"]
        if not legislator_names.isnull().all():
            legislator_name = legislator_names.dropna().iloc[0]
    return f"Legislator: {legislator_name}"
