import pandas as pd
from shiny import module, ui
from htmltools import tags
from faicons import icon_svg as icon


@module.ui
def mod_introduction_ui(data: pd.DataFrame):
    return ui.nav_panel(
        icon("house"),
        ui.card(
            ui.card_header("Welcome to the LGBF dashboard"),
            tags.h6(
                """
                This application presents Local Government Benchmarking
                Framework (LGBF) data collated from local authorities across
                Scotland. This data set combines a set of metrics that enables
                assessment of how well Scottish local authorities are delivering
                services.
                """
            ),
            tags.h6(
                """
                Indicators are categorised into indicator service areas, which
                can be viewed using the 'Indicator Areas' dropdown. Each section
                contains a series of interactive plots visualising each
                indicator and, if applicable, values used to derive this
                indicator.
                """
            ),
            max_height="300px",
        ),
        ui.layout_column_wrap(
            ui.value_box(
                title="Number of local authorities",
                showcase=icon("chart-bar"),
                value=len(pd.unique(data["LA_Information_LocalAuthority"])),
            ),
            ui.value_box(
                title="Number of indicator areas",
                showcase=icon("chart-bar"),
                value=len(pd.unique(data["Indicators_Information_ServiceArea"])),
            ),
            ui.value_box(
                title="Number of indicator categories",
                showcase=icon("chart-bar"),
                value=len(pd.unique(data["Indicators_Information_Category"])),
            ),
            ui.value_box(
                title="Number of indicators",
                showcase=icon("chart-bar"),
                value=len(pd.unique(data["Indicators_Information_Code"])),
            ),
        ),
    )


@module.server
def mod_introduction_server(input, outputm, session, data: pd.DataFrame):
    return True
