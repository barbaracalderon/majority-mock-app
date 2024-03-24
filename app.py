import pandas as pd

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

