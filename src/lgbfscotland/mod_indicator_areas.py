from shiny import module, ui
from lgbfscotland.utils_general import clean_id
from lgbfscotland.indicator_area import indicator_area
from typing import Dict


@module.ui
def mod_indicator_areas_ui(data: Dict[indicator_area]):
    return ui.nav_menu(
        "Indicator Area",
        *[value.mod_ui(clean_id(value.id), value) for key, value in data.items()],
    )


@module.server
def mod_indicator_areas_server(
    input, output, session, data: Dict[indicator_area], is_dark
):
    [
        value.mod_server(clean_id(value.id), value, is_dark=is_dark)
        for key, value in data.items()
    ]
