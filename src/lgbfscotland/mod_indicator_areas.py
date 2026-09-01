from shiny import module, ui
from lgbfscotland.utils_general import clean_id
from lgbfscotland.indicator_area import indicator_area
from typing import Dict


@module.ui
def mod_indicator_areas_ui(data: Dict[indicator_area]):
    """
    Title
    -----
    Indicator area module UI

    Parameters
    ----------
    data: Dict[indicator_area]
        Dictionary of indicator area objects to present
    """
    return ui.nav_menu(
        "Indicator Area",
        *[value.mod_ui(clean_id(value.id), value) for key, value in data.items()],
    )


@module.server
def mod_indicator_areas_server(
    input, output, session, data: Dict[indicator_area], is_dark
):
    """
    Title
    -----
    Indicator area module server

    Parameters
    ----------
    input: Inputs
        Shiny input
    output: Outputs
        Shiny output
    session: Session
        Shiny session
    data: Dict[indicator_area]
        Dictionary of indicator area objects to present
    is_dark: reactive
        Reactive boolean indicating whether app is in dark mode or not
    """
    [
        value.mod_server(clean_id(value.id), value, is_dark=is_dark)
        for key, value in data.items()
    ]
