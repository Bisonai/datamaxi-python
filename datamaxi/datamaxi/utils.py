from typing import List
import pandas as pd


def convert_data_to_data_frame(
    data: List,
    columns_to_replace: List[str] = [],
) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df.set_index("d")

    if len(columns_to_replace) == 0:
        df.replace("NaN", pd.NA, inplace=True)
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    df[columns_to_replace] = df[columns_to_replace].replace("NaN", pd.NA)
    df[columns_to_replace] = df[columns_to_replace].apply(
        pd.to_numeric, errors="coerce"
    )

    return df
