import pandas as pd
from shiny import module, ui, render
from htmltools import tags


@module.ui
def mod_introduction_ui():
    return ui.div(
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
            viewed in the sidebar. Each section contains a series of
            interactive line plots visualising each indicator and values used
            to derive this indicator (if appliable against) time. A datatable
            of the datatable used to produce these figures is also provided.
            """
            ),
        ),
        ui.output_ui("value_boxes"),
        ui.card(
            ui.card_header("References"),
            tags.h5(
                """
            All data used to produce this dashboard was download from the
            Local Government Benchmarking Framework
            """,
                tags.a(
                    "(LGBF) ",
                    href="https://www.improvementservice.org.uk/benchmarking/explore-the-data",
                    target="_blank",
                ),
                "data source.",
            ),
        ),
    )


@module.server
def mod_introduction_server(input, outputm, session, data):
    @render.ui
    def value_boxes():
        boxes = [
            ui.value_box(
                title="Number of local authorities",
                value=len(pd.unique(data["LA_Information_LocalAuthority"])),
            ),
            ui.value_box(
                title="Number of indicator areas",
                value=len(pd.unique(data["Indicators_Information_ServiceArea"])),
            ),
            ui.value_box(
                title="Number of indicator categories",
                value=len(pd.unique(data["Indicators_Information_Category"])),
            ),
            ui.value_box(
                title="Number of indicators",
                value=len(pd.unique(data["Indicators_Information_Code"])),
            ),
        ]
        return ui.layout_column_wrap(*boxes)
