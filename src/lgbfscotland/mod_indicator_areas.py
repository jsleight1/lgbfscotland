from shiny import module, ui, render, req
from htmltools import tags
from loguru import logger
from lgbfscotland.utils_general import clean_id


@module.ui
def mod_indicator_areas_ui():
    return ui.div(
        ui.layout_sidebar(
            ui.sidebar(ui.output_ui("indicator_area_sidebar_content")),
            ui.div(
                ui.card(
                    ui.card_header("Introduction"),
                    tags.h5(
                        """
                        Indicator data for a selected local authority is visualised as
                        a series of interactive line plots. Data are stratified
                        into categories; 'Performance' 'Financial' and 'Satisfaction', which
                        are displayed in independent boxes. Each box contains a
                        menu allowing navigation between different indicator data sets.
                        """
                    ),
                ),
                ui.output_ui("indicator_area_main_content"),
            ),
        )
    )


@module.server
def mod_indicator_areas_server(input, output, session, data):
    @render.ui
    def indicator_area_sidebar_content():
        return ui.input_radio_buttons(
            id="select_content",
            label=None,
            choices=[i.id for i in data.values()],
            inline=False,
        )

    @render.ui
    def indicator_area_main_content():
        req(input.select_content())
        selected_content = input.select_content()
        logger.info(f"Selected {selected_content} content")
        object = data[selected_content]
        object.mod_server(clean_id(selected_content), object)
        output = object.mod_ui(clean_id(selected_content), object)
        return output

    return True
