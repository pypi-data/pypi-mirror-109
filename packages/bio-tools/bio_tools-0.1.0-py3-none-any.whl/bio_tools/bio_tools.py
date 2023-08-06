import pandas as pd


def split_sequences_to_columns(sequences: pd.Series) -> pd.DataFrame:
    return sequences.apply(lambda x: pd.Series(list(x)))
