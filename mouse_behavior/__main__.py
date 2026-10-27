"""Run the exploratory rules on one local tracking CSV."""

import argparse
from pathlib import Path

from .analysis import add_movement_features
from .io import read_tracking_csv


def main():
    parser = argparse.ArgumentParser(description="Apply exploratory movement rules to a tracking CSV.")
    parser.add_argument("--input", type=Path, required=True, help="Existing tracking CSV")
    parser.add_argument("--output", type=Path, required=True, help="New CSV; existing files are never overwritten")
    args = parser.parse_args()
    try:
        result = add_movement_features(read_tracking_csv(args.input))
        result.to_csv(args.output, index=False, mode="x")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Processed {len(result)} rows into {args.output}")
    print("Rule-derived labels:", result["behavior"].value_counts().to_dict())
    print("These labels are illustrative rules, not independent behavioral ground truth.")


if __name__ == "__main__":
    main()
