"""Movement features and the original notebook's illustrative thresholds."""

import numpy as np
import pandas as pd

from .io import REQUIRED


def add_movement_features(data):
    missing = REQUIRED.difference(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    if data.empty:
        raise ValueError("Input data is empty")

    result = data.copy()
    for name in sorted(REQUIRED):
        try:
            values = pd.to_numeric(result[name], errors="raise").astype(float)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} must contain finite numeric values") from exc
        if not np.isfinite(values).all():
            raise ValueError(f"{name} must contain finite numeric values")
        result[name] = values

    frames = result["frame"]
    if (frames < 0).any() or (frames % 1 != 0).any():
        raise ValueError("frame values must be non-negative integers")
    difference = frames.diff()
    if ((difference <= 0) & (frames != 0)).any():
        raise ValueError("frame must increase within each recording; only a reset to 0 marks a new recording")

    reset = (difference <= 0) & (frames == 0)
    dx = result["bodypart1_x"].diff().fillna(0).mask(reset, 0)
    dy = result["bodypart1_y"].diff().fillna(0).mask(reset, 0)
    result["distance"] = np.hypot(dx, dy)
    result["speed"] = result["distance"]  # The notebook assumes one unit of time per sample.
    result["behavior"] = np.select(
        [result["speed"] < 1, (result["distance"] > 10) & (result["speed"] > 5)],
        ["stopping", "exploring"],
        default="moving",
    )
    return result
