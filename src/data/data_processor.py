import pandas as pd
from pandas.core.frame import DataFrame


def merge_data() -> DataFrame:
    bills_df: DataFrame = pd.read_csv("src/data/bills.csv")
    legislators_df: DataFrame = pd.read_csv("src/data/legislators.csv")
    votes_df: DataFrame = pd.read_csv("src/data/votes.csv")
    vote_results_df: DataFrame = pd.read_csv("src/data/vote_results.csv")

    vote_results_merged: DataFrame = pd.merge(
        vote_results_df,
        legislators_df,
        left_on="legislator_id",
        right_on="id",
        suffixes=("_vote", "_legislator"),
    )

    vote_results_merged: DataFrame = pd.merge(
        vote_results_merged,
        votes_df,
        left_on="vote_id",
        right_on="id",
        suffixes=("_vote_results", "_votes"),
    )

    vote_results: DataFrame = pd.merge(
        vote_results_merged,
        bills_df,
        left_on="bill_id",
        right_on="id",
        suffixes=("_votes", "_bills"),
    )

    final_table: DataFrame = pd.merge(
        vote_results,
        legislators_df[["id", "name"]],
        left_on="sponsor_id",
        right_on="id",
        how="left",
    )

    final_table.drop(columns=["id_vote", "id_votes", "id_bills"], inplace=True)
    return final_table


def create_bill_data(data: DataFrame) -> DataFrame:
    bill_data: DataFrame = data.drop(
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
    return bill_data
