import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from copy import deepcopy
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data
from lgbfscotland.utils_general import wrap_text
from shiny import ui, module, render
from shinywidgets import output_widget, render_widget
from loguru import logger


class indicator:
    """
    Title
    -----
    Indicator data object

    Description
    -----------
    Indicator objects contain a DataFrame object storing data for a single
    indicator in a single local authority.

    Examples
    --------
    >>> data = example_lgbf_data().merge(
    >>>   example_lgbf_metadata(),
    >>>   on="Indicators_Information_Code",
    >>>   how="inner"
    >>> )
    >>> data = data[(data["Indicators_Information_Code"] == "SW01") & (data["LA_Information_LocalAuthority"] == "Aberdeen City")]
    >>>
    >>> output = indicator(x=data)
    >>> output
    >>> output.data
    >>> output.id()
    >>> output.title()
    >>> output.authority()
    >>> output.category()
    >>> output.plot(type="indicator")
    >>> output.plot(type="numerator_denominator")
    """

    def __init__(self, x):
        """
        Parameters
        ----------
        x: pandas.core.frame.DataFrame
            A DataFrame of data for single indicator dataset in single local
            authority.
        """
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
        """
        Title
        -----
        Set data attribute for indicator object.

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
        Title
        -----
        Get indicator id.
        """
        return self._assert_unique_col("Indicators_Information_Code")

    def title(self):
        """
        Title
        -----
        Get indicator title.
        """
        return self._assert_unique_col("Indicators_Information_Title")

    def authority(self):
        """
        Title
        -----
        Get indicator authority.
        """
        return self._assert_unique_col("LA_Information_LocalAuthority")

    def category(self):
        """
        Title
        -----
        Get indicator category.
        """
        return self._assert_unique_col("Indicators_Information_Category")

    def _assert_unique_col(self, col):
        output = pd.unique(self.data[col]).tolist()
        assert len(output) == 1, f"'{col}' must have only 1 unique value"
        return output[0]

    def plot(self, type, **kwargs):
        """
        Title
        -----
        Plot indicator object.

        Parameters
        ----------
        type: str
            Type of plot. Either "indicator" or "numerator_denominator"
        **kwargs:
            Passed to plotting methods.

        Examples
        ----------
        >>> x = indicator.example_indicator()
        >>> x.plot(type="indicator")
        """
        match type:
            case "indicator":
                return self._indicator_plot(**kwargs)
            case "numerator_denominator":
                return self._numerator_denominator_plot(**kwargs)
            case _:
                raise Exception(f"{type} plot type not implemented")

    def _indicator_plot(self, is_dark=False, **kwargs):
        data = self._indicator_plot_data()
        unit = pd.unique(data["Indicators_Information_Unit"]).tolist()[0]
        fig = px.line(data, x="Year", y="Metric", color="Category")
        fig = fig.update_xaxes(type="category")
        fig = fig.update_yaxes(
            title_text=wrap_text(self.title()),
            tickformat={"Percentage": ".1%", "Percentage points": ".1%"}.get(unit, ""),
            tickprefix={"Pounds": "£"}.get(unit, ""),
            ticksuffix={"Tonnes": "t", "Days": "days"}.get(unit, ""),
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.5, xanchor="center", x=0.5)
        )
        fig = self._update_fig(fig=fig, is_dark=is_dark)
        return fig

    def _numerator_denominator_plot(self, is_dark=False, **kwargs):
        data = self._numerator_denominator_plot_data()
        num_title = pd.unique(data["Indicators_Information_Numerator_Title"]).tolist()[
            0
        ]
        den_title = pd.unique(
            data["Indicators_Information_Denominator_Title"]
        ).tolist()[0]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = fig.add_trace(
            go.Scatter(
                x=data["LA_Data_LGBF_Year"],
                y=data["LA_Data_LA_Numerator_real"],
                name=num_title,
            ),
            secondary_y=False,
        )
        fig = fig.add_trace(
            go.Scatter(
                x=data["LA_Data_LGBF_Year"],
                y=data["LA_Data_LA_Den_Real"],
                name=den_title,
            ),
            secondary_y=True,
        )
        fig = fig.update_xaxes(title_text="Year", type="category")
        fig = fig.update_yaxes(title_text=wrap_text(num_title), secondary_y=False)
        fig = fig.update_yaxes(title_text=wrap_text(den_title), secondary_y=True)
        fig = fig.update_layout(hovermode="x unified")
        fig.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.5, xanchor="center", x=0.5)
        )
        fig = self._update_fig(fig=fig, is_dark=is_dark)
        return fig

    @staticmethod
    def _update_fig(fig, is_dark=False):
        template = "plotly_dark" if is_dark else "plotly_white"
        text_color = "#f8f9fa" if is_dark else "#212529"
        hover_bg = "#343a40" if is_dark else "#ffffff"
        fig = fig.update_xaxes(
            tickfont=dict(color=text_color),
            linecolor=text_color,
        )
        fig = fig.update_yaxes(
            tickfont=dict(color=text_color),
            linecolor=text_color,
        )
        fig = fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            font=dict(color=text_color),
            title=dict(font=dict(color=text_color)),
            legend_title=dict(font=dict(color=text_color)),
            hoverlabel=dict(
                bgcolor=hover_bg,
                font_color=text_color,
            ),
        )
        return fig

    def _indicator_plot_data(self, **kwargs):
        output = deepcopy(self.data)
        req_cols = {
            "LA_Data_LGBF_Year": "Year",
            "Indicators_Information_Unit": "Indicators_Information_Unit",
            "Indicators_Information_Title": "Indicators_Information_Title",
            "LA_Data_LA_IndicatorReal": "Local Authority",
            "Scotland_Data_Scotland_Indicator_Real": "Scotland",
            "FG_Data_FG_Avg_Indicator_Real": "Family Group",
        }
        output = output.rename(columns=req_cols)[req_cols.values()]
        output = output.melt(
            id_vars=["Year", "Indicators_Information_Unit"],
            value_vars=["Local Authority", "Family Group", "Scotland"],
            var_name="Category",
            value_name="Metric",
        )
        return output

    def _numerator_denominator_plot_data(self, **kwargs):
        output = deepcopy(self.data)
        req_cols = [
            "Indicators_Information_Code",
            "LA_Information_LocalAuthority",
            "LA_Data_LGBF_Year",
            "LA_Data_LA_Numerator_real",
            "LA_Data_LA_Den_Real",
            "Indicators_Information_Numerator_Title",
            "Indicators_Information_Denominator_Title",
        ]
        return output[req_cols]

    def summary(self, type, **kwargs):
        """
        Title
        -----
        Summarise indicator object.

        Parameters
        ----------
        type: str
            Type of summary. Options are "indicator".
        **kwargs:
            Passed to summary methods.

        Examples
        ----------
        >>> x = indicator.example_indicator()
        >>> x.summary(type="indicator")
        """
        match type:
            case "indicator":
                return self._indicator_summary(**kwargs)
            case _:
                raise Exception(f"{type} summary type not implemented")

    def _indicator_summary(self):
        cols = {
            "Indicators_Information_Code": "Indicators Code",
            "LA_Data_LGBF_Year": "Year",
            "LA_Data_LA_IndicatorReal": "Indicator value",
            "LA_Data_LA_Numerator_real": "Indicator numerator value",
            "LA_Data_LA_Den_Real": "Indicator denominator value",
            "Scotland_Data_Scotland_Indicator_Real": "Scotland indicator value",
            "Scotland_Data_Scotland_Num_Real": "Scotland indicator numerator value",
            "Scotland_Data_Scotland_Den_Real": "Scotland indicator denominator value",
            "FG_Data_FG_Avg_Indicator_Real": "Family group indicator value",
            "FG_Data_FG_Avg_Num_Real": "Family group indicator numerator value",
            "FG_Data_FG_Avg_Den_Real": "Family group indicator denominator value",
        }
        return self.data.rename(columns=cols)[cols.values()]

    @staticmethod
    @module.ui
    def mod_ui(object):
        return ui.nav_panel(
            object.title(),
            ui.div(
                ui.card_header(object.title()),
                ui.output_ui("indicator_ui"),
                min_height="500px",
            ),
        )

    @staticmethod
    @module.server
    def mod_server(input, output, session, object, is_dark):
        @render_widget
        def indicator_plot():
            logger.info("Creating indicator plot")
            return object.plot(type="indicator", is_dark=is_dark() == "dark")

        @render_widget
        def numerator_denominator_plot():
            logger.info("Creating numerator denominator indicator plot")
            return object.plot(
                type="numerator_denominator", is_dark=is_dark() == "dark"
            )

        @render.data_frame
        def indicator_table():
            logger.info("Creating indicator summary")
            return render.DataTable(
                object.summary(type="indicator"), filters=True, width="100%"
            )

        @render.download(filename=f"{object.title()}.csv")
        def download_indicator_table():
            logger.info("Downloading indicator summary")
            filtered_df = indicator_table.data_view()
            yield filtered_df.to_csv(index=False)

        @render.ui
        def indicator_ui():
            num_den_widget = None
            col_widths = [12, 1]
            if object._contains_num_den():
                num_den_widget = output_widget("numerator_denominator_plot")
                col_widths = [6, 6]
            return ui.navset_tab(
                ui.nav_panel(
                    "Plot",
                    ui.layout_columns(
                        output_widget("indicator_plot"),
                        num_den_widget,
                        col_widths=col_widths,
                    ),
                ),
                ui.nav_panel(
                    "Table",
                    ui.output_data_frame("indicator_table"),
                    ui.download_button(
                        "download_indicator_table",
                        "Download CSV",
                    ),
                ),
            )

    def _contains_num_den(self):
        return not (
            pd.isna(self.data["LA_Data_LA_Numerator_real"]).all()
            and pd.isna(self.data["LA_Data_LA_Den_Real"]).all()
        )

    @staticmethod
    def example_indicator():
        """
        Title
        -----
        Generate example indicator object

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
