import importlib.metadata
import pandas as pd
from lgbfscotland.utils_config import settings
from lgbfscotland.utils_data_processing import load_lgbf_data
from lgbfscotland.indicator import indicator
from lgbfscotland.indicator_area import indicator_area
from lgbfscotland.mod_introduction import mod_introduction_ui
from lgbfscotland.mod_indicator_areas import (
    mod_indicator_areas_ui,
    mod_indicator_areas_server,
)
from lgbfscotland.mod_about import mod_about_ui
from loguru import logger
from faicons import icon_svg as icon
from shiny import ui, App

def lgbfscotland(**kwargs):
    """
    Launch lgbfscotland shiny app.

    Parameters
    ----------
    **kwargs
        Passed to shiny.App.
    """
    logger.info(f"Running lgbfscotland in {settings.type} mode")
    lgbf_data = load_lgbf_data(settings)
    indicator_areas = create_indicator_areas(lgbf_data)
    app_ui = ui.page_navbar(
        mod_introduction_ui("introduction", data=lgbf_data),
        mod_indicator_areas_ui("indicator_areas", data=indicator_areas),
        ui.nav_spacer(),
        mod_about_ui("about"),
        ui.nav_control(
            ui.a(
                icon("linkedin"),
                href="https://www.linkedin.com/in/jack-sleight-461a6699/",
                target="_blank",
            )
        ),
        ui.nav_control(
            ui.a(
                icon("github"),
                href="https://github.com/jsleight1/lgbfscotland",
                target="_blank",
            )
        ),
        ui.nav_control(ui.input_dark_mode(id="mode")),
        ui.nav_control(
            ui.a("v" + importlib.metadata.version("LGBFScotland"), class_="navbar_text")
        ),
        title=ui.tags.span("LGBFScotland"),
        theme=ui.Theme.from_brand(__file__),
        fillable=True,
        footer=ui.div("Created by Jack Sleight", class_="footer"),
    )

    def server(input, output, session):
        mod_indicator_areas_server(
            "indicator_areas", data=indicator_areas, is_dark=input.mode
        )

    return App(ui=app_ui, server=server, **kwargs)


def create_indicator_areas(x: pd.DataFrame):
    service_areas = [
        group for _, group in x.groupby("Indicators_Information_ServiceArea")
    ]
    indicator_areas = {}
    for i in service_areas:
        name = pd.unique(i["Indicators_Information_ServiceArea"]).tolist()[0]
        grps = ["Indicators_Information_Code", "LA_Information_LocalAuthority"]
        output = indicator_area(
            x=[indicator(group) for _, group in i.groupby(grps)],
            id=pd.unique(i["Indicators_Information_ServiceArea"]).tolist()[0],
        )
        indicator_areas[name] = output
    return indicator_areas
