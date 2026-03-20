import pytest
from lgbfscotland.indicator import indicator
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data
from copy import deepcopy
import pandas as pd

metadata = example_lgbf_metadata()
data = example_lgbf_data()
indicator_data = data.merge(metadata, on="Indicators_Information_Code", how="inner")
indicator_data = indicator_data[indicator_data["Indicators_Information_Code"] == "SW01"]
indicator_data = indicator_data[
    indicator_data["LA_Information_LocalAuthority"] == "Aberdeen City"
]


def test_indicator_generation(snapshot):
    output = indicator(indicator_data)
    assert isinstance(output, indicator)
    assert output.id() == "SW01"
    assert output.title() == "Home care costs per hour for people aged 65 or over"
    assert output.authority() == "Aberdeen City"
    assert output.category() == "Financial"
    snapshot.assert_match(str(output), "indicator_generation.txt")


def test_indicator_validation():
    test_data = deepcopy(indicator_data)
    test_data["Indicators_Information_Code"] = ["a", "b"]

    with pytest.raises(AssertionError) as err:
        indicator(test_data)
    assert "'Indicators_Information_Code' must have only 1 unique value" in str(
        err.value
    )

    test_data["Indicators_Information_Code"] = ["a", "a"]
    test_data["Indicators_Information_Title"] = ["a", "b"]
    with pytest.raises(AssertionError) as err:
        indicator(test_data)
    assert "'Indicators_Information_Title' must have only 1 unique value" in str(
        err.value
    )

    test_data["Indicators_Information_Title"] = ["a", "a"]
    test_data["LA_Information_LocalAuthority"] = ["a", "b"]
    with pytest.raises(AssertionError) as err:
        indicator(test_data)
    assert "'LA_Information_LocalAuthority' must have only 1 unique value" in str(
        err.value
    )

    test_data["LA_Information_LocalAuthority"] = ["a", "a"]
    test_data["Indicators_Information_Category"] = ["a", "b"]
    with pytest.raises(AssertionError) as err:
        indicator(test_data)
    assert "'Indicators_Information_Category' must have only 1 unique value" in str(
        err.value
    )

    test_data["Indicators_Information_Category"] = ["a", "a"]
    test_data = test_data.drop(columns=["Scotland_Data_Scotland_Indicator_Real"])
    with pytest.raises(AssertionError) as err:
        indicator(test_data)
    assert "Missing columns" in str(err.value)


def test_plot_indicator(snapshot):
    x = indicator.example_indicator()
    with pytest.raises(TypeError) as err:
        x.plot()
    assert "indicator.plot() missing 1 required positional argument: 'type'" in str(
        err.value
    )


def test_indicator_properties():
    output = indicator.example_indicator()
    with pytest.raises(AssertionError) as err:
        output.data = 1
    assert "data is not DataFrame" in str(err.value)


def test_example_indicator(snapshot):
    output = indicator.example_indicator()
    assert isinstance(output, indicator)
    snapshot.assert_match(str(output), "example_indicator.txt")
