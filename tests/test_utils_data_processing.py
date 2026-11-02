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

    def mock_data_get(x, **kwargs):
        return data_map.get(x)

    mock = mocker.patch(
        "lgbfscotland.utils_data_processing._read_bytes_csv", side_effect=mock_data_get
    )
    output = process_lgbf_data("metadata", "data")
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (8, 18)
    assert mock.call_args_list == [
        mocker.call("metadata", encoding="ISO-8859-1"),
        mocker.call("data"),
    ]
    snapshot.assert_match(str(output), "process_lgbf_data.txt")


def test_save_lgbf_data(mocker):
    settings = test_settings("development")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing._save_local_lgbf_data", return_value=True
    )
    output = save_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(data="data")
    settings = test_settings("production")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing._save_azure_lgbf_data", return_value=True
    )
    output = save_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(data="data")


def test_load_lgbf_data(mocker):
    settings = test_settings("development")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing._load_local_lgbf_data", return_value=True
    )
    output = load_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(settings=settings, data="data")
    settings = test_settings("production")
    mock = mocker.patch(
        "lgbfscotland.utils_data_processing._load_azure_lgbf_data", return_value=True
    )
    output = load_lgbf_data(settings=settings, data="data")
    assert output
    mock.assert_called_once_with(settings=settings, data="data")
