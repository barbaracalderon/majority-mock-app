from data import bill_data
from dash import Input, Output, callback
from typing import Any, Dict, List, Union
import pandas as pd


def update_bill_graph(
    value: str,
) -> Dict[
    str, Union[List[Dict[str, Union[str, List[int]]]], Dict[str, Dict[str, str]]]
]:
    bill_filtered_data: pd.DataFrame = bill_data[bill_data["title"] == value]
    x_values: List[str] = bill_filtered_data["position"].unique()
    y_values: List[int] = [
        bill_filtered_data[bill_filtered_data["position"] == x_val].shape[0]
        for x_val in x_values
    ]

    fig: Dict[
        str, Union[List[Dict[str, Union[str, List[int]]]], Dict[str, Dict[str, str]]]
    ] = {
        "data": [{"type": "bar", "x": x_values, "y": y_values, "name": "Count"}],
        "layout": {
            "title": "Number of votes for the selected bill",
            "xaxis": {"title": "Position taken"},
            "yaxis": {"title": "Number of votes"},
        },
    }
    return fig


def update_legislator_graph(
    value: str,
) -> Dict[
    str, Union[List[Dict[str, Union[str, List[int]]]], Dict[str, Dict[str, str]]]
]:
    legislator_filtered_data: pd.DataFrame = bill_data[bill_data["legislator"] == value]
    x_values: List[str] = legislator_filtered_data["position"].unique()
    y_values: List[int] = [
        legislator_filtered_data[legislator_filtered_data["position"] == x_val].shape[0]
        for x_val in x_values
    ]

    fig: Dict[
        str, Union[List[Dict[str, Union[str, List[int]]]], Dict[str, Dict[str, str]]]
    ] = {
        "data": [{"type": "bar", "x": x_values, "y": y_values, "name": "Count"}],
        "layout": {
            "title": "Overall position in bills",
            "xaxis": {"title": "Position taken"},
            "yaxis": {"title": "Number of bills"},
        },
    }
    return fig
