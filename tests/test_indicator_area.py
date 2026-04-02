import pytest
from lgbfscotland.indicator import indicator
from lgbfscotland.indicator_area import indicator_area
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data
from shiny import ui

metadata = example_lgbf_metadata()
data = example_lgbf_data()
indicator_data = data.merge(metadata, on="Indicators_Information_Code", how="inner")
grps = ["Indicators_Information_Code", "LA_Information_LocalAuthority"]
indicators = [indicator(group) for _, group in indicator_data.groupby(grps)]


def test_indicator_area_generation(snapshot):
    output = indicator_area(x=indicators, id="id")
    assert isinstance(output, indicator_area)
    assert output.id == "id"
    assert all([isinstance(i, indicator) for i in output.data])
    snapshot.assert_match(str(output), "indicator_area_generation.txt")
    snapshot.assert_match(str(output.data), "indicator_area_generation_data.txt")


def test_indicator_area_validation():
    with pytest.raises(AssertionError) as err:
        indicator_area(x=indicators, id=1)
    assert "id must be a string" in str(err.value)

    with pytest.raises(AssertionError) as err:
        indicator_area([1, 2], id="id")
    assert "indicator area objects must only contain indicator objects" in str(
        err.value
    )


def test_indicator_area_properties():
    output = indicator_area.example_indicator_area()
    with pytest.raises(AssertionError) as err:
        output.id = 1
    assert "id must be a string" in str(err.value)
    with pytest.raises(AssertionError) as err:
        output.data = 1
    assert "data is not list" in str(err.value)
    with pytest.raises(AssertionError) as err:
        output.data = [1, 2]
    assert "indicator area objects must only contain indicator objects" in str(
        err.value
    )


def test_indicator_area_modules():
    x = indicator_area.example_indicator_area()
    output = x.mod_ui("indicator", x)
    assert isinstance(output, ui._navs.NavPanel)


def test_example_indicator_area(snapshot):
    output = indicator_area.example_indicator_area()
    assert isinstance(output, indicator_area)
    snapshot.assert_match(str(output), "example_indicator_area.txt")
