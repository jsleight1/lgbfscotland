import pandas as pd
from copy import deepcopy
from lgbfscotland.indicator import indicator
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data
from lgbfscotland.utils_general import clean_id
from shiny import ui, module, req, render
from faicons import icon_svg as icon
from loguru import logger
from htmltools import tags


class indicator_area:
    """
    Title
    -----
    Indicator area object

    Description
    -----------
    Indicator area objects contain a list of Indicator objects for a single
    indicator service area in a single local authority.

    Examples
    --------
    >>> data = indicator.example_indicator()
    >>> output = indicator_area(data = [data], id = "area")
    >>> output
    >>> output.data
    >>> output.id
    """

    def __init__(self, x: list[indicator], id: str):
        """
        Parameters
        ----------
        x: list
            A list of indicator objects.
        id: str
            A string Id for indicator area object.
        """
        self._data = deepcopy(x)
        self._id = id
        self._validate()

    def __str__(self):
        output = f"""
        Indicator area object
        - id: {self.id}
        - N indicators: {len(self.data)}
        """
        return output

    def __repr__(self):
        output = f"""
        Indicator area object
        - id: {self.id}
        - N indicators: {len(self.data)}
        """
        return output

    def _get_data(self):
        return self._data

    def _set_data(self, value: list[indicator]):
        """
        Title
        -----
        Set data attribute for indicator object.

        Parameters
        ----------
        value: list
            A list of indicator objects.
        """
        assert isinstance(value, list), "data is not list"
        assert all([isinstance(i, indicator) for i in value]), (
            "indicator area objects must only contain indicator objects"
        )
        self._data = deepcopy(value)

    data = property(_get_data, _set_data)

    def _get_id(self):
        return self._id

    def _set_id(self, value: str):
        """
        Title
        -----
        Set id attribute for indicator area object.

        Parameters
        ----------
        value: string
            A string id.
        """
        assert isinstance(value, str), "id must be a string string"
        self._id = deepcopy(value)

    id = property(_get_id, _set_id)

    def _validate(self):
        assert isinstance(self.id, str), "id must be a string"
        assert all([isinstance(i, indicator) for i in self.data]), (
            "indicator area objects must only contain indicator objects"
        )

    @staticmethod
    @module.ui
    def mod_ui(object: indicator_area):
        authorities = [i.authority() for i in object.data]
        return ui.nav_panel(
            object.id,
            ui.card(
                ui.card_header(object.id),
                tags.h6(
                    """
                    Indicator data for a selected local authority is
                    visualised as a series of interactive line plots.
                    Data are stratified into categories; 'Performance'
                    'Financial' and 'Satisfaction', which are displayed
                    in independent boxes. Each box contains a menu
                    allowing navigation between different indicator data
                    sets.
                    """
                ),
                tags.h6(
                    "The ",
                    ui.a(
                        "LGBF",
                        href="https://www.improvementservice.org.uk/benchmarking/home",
                        target="_blank",
                    ),
                    """
                     describes the process of how these metrics have been
                    developed and how councils have been organised into 'family
                    groups'. This essentially means that similar councils in
                    terms of levels of deprivation and population are compared
                    to each other. Indicator data is visualised as a series of
                    interactive plots and tables showing the indicator value for
                    a selected local authority alongside the indicator value
                    summarisied by council family group and nationally across
                    Scotland. The values used to derive the indicator metric,
                    if applicable, are also presented.
                    """,
                ),
                ui.input_select(
                    id="select_authority",
                    label="Select authority",
                    choices=authorities,
                    selected=authorities[0],
                ),
                ui.output_ui("indicator_boxes"),
            ),
        )

    @staticmethod
    @module.server
    def mod_server(input, output, session, object: indicator_area, is_dark):
        @render.ui
        def indicator_boxes():
            req(input.select_authority)
            selected_authority = input.select_authority()
            logger.info(f"Selected {selected_authority}")
            data = object._split_by_category(selected_authority)
            output = []
            for key, value in data.items():
                indicators = [ind for ind in value["data"].tolist()]
                output += [
                    ui.navset_card_tab(
                        ui.nav_spacer(),
                        ui.nav_menu(
                            "Select indicator",
                            *[
                                ind.mod_ui(clean_id(ind.id()), ind)
                                for ind in indicators
                            ],
                        ),
                        title=key,
                    )
                ]
                [ind.mod_server(clean_id(ind.id()), ind, is_dark) for ind in indicators]
            return ui.div(*output)

    def _split_by_category(self, authority: str):
        output = [i for i in self.data if i.authority() == authority]
        output = pd.DataFrame(
            {"category": [i.category() for i in output], "data": output}
        )
        output = {name: group for name, group in output.groupby("category")}
        return output

    @staticmethod
    def example_indicator_area():
        metadata = example_lgbf_metadata()
        data = example_lgbf_data()
        indicator_data = data.merge(
            metadata, on="Indicators_Information_Code", how="inner"
        )
        grps = ["Indicators_Information_Code", "LA_Information_LocalAuthority"]
        output = indicator_area(
            x=[indicator(group) for _, group in indicator_data.groupby(grps)],
            id="service_area",
        )
        return output
