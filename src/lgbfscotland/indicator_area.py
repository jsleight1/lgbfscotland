from copy import deepcopy
from lgbfscotland.indicator import indicator
from lgbfscotland.utils_example_data import example_lgbf_metadata, example_lgbf_data
from shiny import ui, module, render
from htmltools import tags


class indicator_area:
    def __init__(self, data, id):
        self._data = deepcopy(data)
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

    def _set_data(self, value: list):
        """Set data attribute for indicator object.

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
        """Set id attribute for indicator area object.

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
    def mod_ui(object):
        authorities = ["a"]
        return ui.div(
            ui.card(
                ui.card_header(object.id),
                ui.input_select(
                    id="authority_select",
                    label="Select authority",
                    choices=authorities,
                    selected=authorities[0],
                ),
                ui.output_ui("indicator_boxes"),
            )
        )

    @staticmethod
    @module.server
    def mod_server(input, output, session, object):
        @render.ui
        def indicator_boxes():
            return ui.div(tags.h4(object.id))

        return True

    @staticmethod
    def example_indicator_area():
        metadata = example_lgbf_metadata()
        data = example_lgbf_data()
        indicator_data = data.merge(
            metadata, on="Indicators_Information_Code", how="inner"
        )
        grps = ["Indicators_Information_Code", "LA_Information_LocalAuthority"]
        output = indicator_area(
            data=[indicator(group) for _, group in indicator_data.groupby(grps)],
            id="service_area",
        )
        return output
