from shiny import App
from lgbfscotland.lgbfscotland import app_ui, server

app = App(ui=app_ui, server=server)
