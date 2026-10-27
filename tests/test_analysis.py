import numpy as np
import pandas as pd
import pytest

from mouse_behavior.analysis import add_movement_features


def test_rule_thresholds_follow_the_original_notebook():
    data = pd.DataFrame({
        "frame": [0, 1, 2, 3, 4],
        "bodypart1_x": [0, 0.5, 1.5, 11.5, 21.5001],
        "bodypart1_y": [0, 0, 0, 0, 0],
    })
    result = add_movement_features(data)
    np.testing.assert_allclose(result["distance"], [0, 0.5, 1, 10, 10.0001])
    np.testing.assert_allclose(result["speed"], result["distance"])
    assert result["behavior"].tolist() == ["stopping", "stopping", "moving", "moving", "exploring"]
    assert "distance" not in data.columns


def test_new_recording_does_not_connect_positions_across_frame_reset():
    data = pd.DataFrame({
        "frame": [0, 1, 0, 1],
        "bodypart1_x": [0, 3, 100, 104],
        "bodypart1_y": [0, 0, 100, 100],
    })
    result = add_movement_features(data)
    np.testing.assert_allclose(result["distance"], [0, 3, 0, 4])


@pytest.mark.parametrize("frames", [[0, 1, 1], [0, 2, 1], [0, -1], [0, 1.5]])
def test_invalid_frames_are_rejected(frames):
    data = pd.DataFrame({"frame": frames, "bodypart1_x": [0] * len(frames), "bodypart1_y": [0] * len(frames)})
    with pytest.raises(ValueError, match="frame"):
        add_movement_features(data)


@pytest.mark.parametrize("bad", [np.nan, np.inf, "invalid"])
def test_invalid_coordinates_are_rejected(bad):
    data = pd.DataFrame({"frame": [0], "bodypart1_x": [bad], "bodypart1_y": [0]})
    with pytest.raises(ValueError, match="bodypart1_x"):
        add_movement_features(data)


def test_missing_columns_and_empty_input_are_rejected():
    with pytest.raises(ValueError, match="bodypart1_y"):
        add_movement_features(pd.DataFrame({"frame": [0], "bodypart1_x": [1]}))
    with pytest.raises(ValueError, match="empty"):
        add_movement_features(pd.DataFrame(columns=["frame", "bodypart1_x", "bodypart1_y"]))
