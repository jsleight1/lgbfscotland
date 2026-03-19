from shiny import App
from LGBFScotland.LGBFScotland import app_ui, server

app = App(ui=app_ui, server=server)
