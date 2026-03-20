import importlib.metadata
from lgbfscotland.utils_config import settings
from lgbfscotland.utils_data_processing import load_lgbf_data
from loguru import logger
from shiny import ui

app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_control(ui.input_dark_mode(id="colour_mode")),
    ui.nav_control("v" + importlib.metadata.version("LGBFScotland")),
    title=ui.tags.span("LGBFScotland"),
    fillable=True,
    footer=ui.div("Created by Jack Sleight", class_="footer"),
)


def server(input, output, session):
    lgbf_data = load_lgbf_data(settings)
    logger.info(f"Running lgbfscotland in {settings.type} mode")
    return True
