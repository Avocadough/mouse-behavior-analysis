import subprocess
import sys

import pandas as pd
import pytest

from mouse_behavior.io import read_tracking_csv


def test_clean_and_deeplabcut_headers_are_read(tmp_path):
    clean = tmp_path / "clean.csv"
    clean.write_text("frame,bodypart1_x,bodypart1_y\n0,1,2\n", encoding="utf-8")
    assert read_tracking_csv(clean).loc[0, "bodypart1_x"] == 1

    raw = tmp_path / "raw.csv"
    raw.write_text(
        "scorer," + ",".join(["DLC"] * 12) + "\n"
        "bodyparts," + ",".join(["bodypart1"] * 3 + ["bodypart2"] * 3 + ["bodypart3"] * 3 + ["objectA"] * 3) + "\n"
        "coords," + ",".join(["x", "y", "likelihood"] * 4) + "\n"
        "0," + ",".join(["1", "2", "0.9"] * 4) + "\n",
        encoding="utf-8",
    )
    frame = read_tracking_csv(raw)
    assert frame.loc[0, "bodypart1_x"] == 1
    assert frame.loc[0, "bodypart1_y"] == 2
    assert len(frame) == 1


def test_unknown_headers_are_not_silently_reinterpreted(tmp_path):
    source = tmp_path / "invalid.csv"
    source.write_text("x,y\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="columns"):
        read_tracking_csv(source)


def test_cli_creates_output_and_will_not_overwrite(tmp_path):
    source = tmp_path / "input.csv"
    output = tmp_path / "output.csv"
    source.write_text("frame,bodypart1_x,bodypart1_y\n0,0,0\n1,3,4\n", encoding="utf-8")
    command = [sys.executable, "-m", "mouse_behavior", "--input", str(source), "--output", str(output)]
    first = subprocess.run(command, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    assert pd.read_csv(output)["distance"].tolist() == [0, 5]
    before = output.read_bytes()
    second = subprocess.run(command, capture_output=True, text=True)
    assert second.returncode != 0
    assert output.read_bytes() == before
