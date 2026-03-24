import pytest
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data
import pandas as pd


def test_example_lgbf_metadata():
    cols = [
        "Indicators_Information_Code",
        "Indicators_Information_Title",
        "Indicators_Information_ServiceArea",
        "Indicators_Information_Numerator_Title",
        "Indicators_Information_Denominator_Title",
        "Indicators_Information_Unit",
        "Indicators_Information_Category",
    ]
    output = example_lgbf_metadata()
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (2, 7)
    assert output.columns.tolist() == cols


def test_example_lgbf_data():
    cols = [
        "Indicators_Information_Code",
        "LA_Information_LocalAuthority",
        "LA_Data_LGBF_Year",
        "LA_Data_LA_IndicatorReal",
        "LA_Data_LA_Numerator_real",
        "LA_Data_LA_Den_Real",
        "Scotland_Data_Scotland_Indicator_Real",
        "Scotland_Data_Scotland_Num_Real",
        "Scotland_Data_Scotland_Den_Real",
        "FG_Data_FG_Avg_Indicator_Real",
        "FG_Data_FG_Avg_Num_Real",
        "FG_Data_FG_Avg_Den_Real",
    ]
    output = example_lgbf_data()
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (8, 12)
    assert output.columns.tolist() == cols
