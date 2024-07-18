from typing import List
import pandas as pd


def convert_data_to_data_frame(data: List) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df.set_index("d")
    df.replace("NaN", pd.NA, inplace=True)
    df = df.apply(pd.to_numeric, errors="coerce")
    return df
