import pytest
import pandas as pd
from lgbfscotland.utils_data_processing import (
    process_lgbf_data,
    save_lgbf_data,
    load_lgbf_data,
)
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data


class test_settings:
    def __init__(self, type):
        self.type = type


def test_process_lgbf_data(snapshot, mocker):
    data_map = {"metadata": example_lgbf_metadata(), "data": example_lgbf_data()}
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing.read_bytes_csv",
        side_effect=lambda x: data_map.get(x),
    )
    output = process_lgbf_data("metadata", "data")
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (8, 18)
    assert mock.call_args_list == [mocker.call("metadata"), mocker.call("data")]
    snapshot.assert_match(str(output), "process_lgbf_data.txt")


def test_save_lgbf_data(mocker):
    settings = test_settings("development")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing.save_local_lgbf_data", return_value=True
    )
    output = save_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(data="data")
    settings = test_settings("production")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing.save_azure_lgbf_data", return_value=True
    )
    output = save_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(data="data")


def test_load_lgbf_data(mocker):
    settings = test_settings("development")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing.load_local_lgbf_data", return_value=True
    )
    output = load_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(settings=settings, data="data")
    settings = test_settings("production")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing.load_azure_lgbf_data", return_value=True
    )
    output = load_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(settings=settings, data="data")
