import pandas as pd
from shiny import module, ui
from htmltools import tags
from faicons import icon_svg as icon


@module.ui
def mod_introduction_ui(data):
    return ui.nav_panel(
        icon("house"),
        ui.card(
            ui.card_header("Welcome to the LGBF dashboard"),
            tags.h5(
                """
            This dashboard presents a summary of local authority indicator
            data obtained from the Local Government Benchmarking Framework
            (LGBF). The dashboard aims to consolidate indicator data across
            Scotland's local authorities to understand how effective they
            are delivering services.
            """
            ),
            tags.h5(
                """
            Indicators are categorised into indicator service areas, which can be
            viewed using the 'Indicator Areas' dropdown. Each section contains a series of
            interactive line plots visualising each indicator and values used
            to derive this indicator (if applicable) against time.
            """
            ),
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
        ui.card(
            ui.card_header("References"),
            tags.h6(
                """
            All data used to produce this data is available from the
            Local Government Benchmarking Framework
            """,
                tags.a(
                    "(LGBF)",
                    href="https://www.improvementservice.org.uk/benchmarking/explore-the-data",
                    target="_blank",
                ),
                """
                . Specifically data was download from the 'LGBF indicators information'
                and 'LGBF Data Table Real' data sets avaiable for download from the
                """,
                tags.a(
                    "'Spatial Hub'",
                    href="https://data.spatialhub.scot/dataset/local_government_benchmarking_framework-is",
                    target="_blank",
                ),
                """
                which is licensed under a UK Open Government Licence (OGL) license.
                """,
            ),
        ),
    )


@module.server
def mod_introduction_server(input, outputm, session, data):
    return True
