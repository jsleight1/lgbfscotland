import pandas as pd
from copy import deepcopy
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data


class indicator:
    def __init__(self, x):
        self._data = deepcopy(x)
        self._validate()

    def __str__(self):
        output = f"""
        Indicator object
        - id: {self.id()}
        - title: {self.title()}
        - authority: {self.authority()}
        - category: {self.category()}
        - Dimensions: {self.data.shape[1]} x {self.data.shape[0]}
        """
        return output

    def __repr__(self):
        output = f"""
        Indicator object
        - id: {self.id()}
        - title: {self.title()}
        - authority: {self.authority()}
        - category: {self.category()}
        - Dimensions: {self.data.shape[1]} x {self.data.shape[0]}
        """
        return output

    def _get_data(self):
        return self._data

    def _set_data(self, value: pd.DataFrame):
        """Set data attribute for indicator object.

        Parameters
        ----------
        value: pandas.core.frame.DataFrame
            A DataFrame of indicator data
        """
        assert isinstance(value, pd.DataFrame), "data is not DataFrame"
        self._data = deepcopy(value)

    data = property(_get_data, _set_data)

    def _validate(self):
        assert isinstance(self.data, pd.DataFrame), "data is not DataFrame"
        assert isinstance(self.id(), str), "id must be string"
        assert isinstance(self.title(), str), "title must be string"
        assert isinstance(self.authority(), str), "authority must be string"
        assert isinstance(self.category(), str), "category must be string"
        req_cols = indicator._required_indicator_cols()
        assert set(req_cols).issubset(self.data.columns), (
            "Missing columns. 'See _required_indicator_cols' for all required columns"
        )

    @staticmethod
    def _required_indicator_cols():
        return [
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
            "Indicators_Information_Unit",
            "Indicators_Information_Title",
            "Indicators_Information_Code",
            "Indicators_Information_Numerator_Title",
            "Indicators_Information_Denominator_Title",
            "Indicators_Information_Category",
        ]

    def id(self):
        """
        Get indicator id.
        """
        return self._assert_unique_col("Indicators_Information_Code")

    def title(self):
        """
        Get indicator title.
        """
        return self._assert_unique_col("Indicators_Information_Title")

    def authority(self):
        """
        Get indicator authority.
        """
        return self._assert_unique_col("LA_Information_LocalAuthority")

    def category(self):
        """
        Get indicator category.
        """
        return self._assert_unique_col("Indicators_Information_Category")

    def _assert_unique_col(self, col):
        output = pd.unique(self.data[col]).tolist()
        assert len(output) == 1, f"'{col}' must have only 1 unique value"
        return output[0]

    @staticmethod
    def example_indicator():
        """Generate example indicator object

        Returns
        ----------
        indicator object.

        Examples
        ----------
        >>> x = indicator.example_indicator()
        >>> print(x)
        """
        metadata = example_lgbf_metadata()
        data = example_lgbf_data()
        output = data.merge(metadata, on="Indicators_Information_Code", how="inner")
        output = output[output["Indicators_Information_Code"] == "SW01"]
        output = output[output["LA_Information_LocalAuthority"] == "Aberdeen City"]
        return indicator(x=output)
