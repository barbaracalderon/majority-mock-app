import pandas as pd
from pandas import DataFrame


class DataProcessor:

    def __init__(self):
        self.table: DataFrame = None

    def create_table(self) -> None:
        self.table = self.__merge_dataframes()

    def __load_data(self, path: str) -> DataFrame:
        table_df: DataFrame = pd.read_csv(path)
        return table_df

    def __merge_dataframes(self) -> DataFrame:
        bills_df: DataFrame = self.__load_data("models/bills.csv")
        legislators_df: DataFrame = self.__load_data("models/legislators.csv")
        vote_results_df: DataFrame = self.__load_data("models/vote_results.csv")
        votes_df: DataFrame = self.__load_data("models/votes.csv")

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

        final_merge_table: DataFrame = pd.merge(
            vote_results,
            legislators_df[["id", "name"]],
            left_on="sponsor_id",
            right_on="id",
            how="left",
        )

        final_clean_table: DataFrame = self.__drop_unnused_columns(final_merge_table)
        return final_clean_table

    def __drop_unnused_columns(self, table: DataFrame) -> DataFrame:
        table.drop(columns=["id_vote", "id_votes", "id_bills"], inplace=True)
        return table
