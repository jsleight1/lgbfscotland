from shiny import module, ui
from lgbfscotland.utils_general import clean_id


@module.ui
def mod_indicator_areas_ui(data):
    return ui.nav_menu(
        "Indicator Area",
        *[value.mod_ui(clean_id(value.id), value) for key, value in data.items()],
    )


@module.server
def mod_indicator_areas_server(input, output, session, data, is_dark):
    [
        value.mod_server(clean_id(value.id), value, is_dark=is_dark)
        for key, value in data.items()
    ]
