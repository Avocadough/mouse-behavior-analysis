"""Read the two tracking CSV layouts present in this repository."""

import pandas as pd


COLUMNS = ["frame"] + [
    f"{part}_{coordinate}"
    for part in ("bodypart1", "bodypart2", "bodypart3", "objectA")
    for coordinate in ("x", "y", "likelihood")
]
REQUIRED = {"frame", "bodypart1_x", "bodypart1_y"}


def read_tracking_csv(path):
    data = pd.read_csv(path)
    if REQUIRED.issubset(data.columns):
        return data

    parts = [part for part in ("bodypart1", "bodypart2", "bodypart3", "objectA") for _ in range(3)]
    coordinates = [coordinate for _ in range(4) for coordinate in ("x", "y", "likelihood")]
    if (
        len(data.columns) == len(COLUMNS)
        and data.columns[0] == "scorer"
        and len(data) >= 2
        and data.iloc[0].tolist() == ["bodyparts", *parts]
        and data.iloc[1].tolist() == ["coords", *coordinates]
    ):
        data = data.iloc[2:].copy().reset_index(drop=True)
        data.columns = COLUMNS
        return data.apply(pd.to_numeric, errors="raise")

    raise ValueError("CSV columns must contain frame, bodypart1_x and bodypart1_y, or a supported DeepLabCut header")
