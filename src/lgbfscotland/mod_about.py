from shiny import module, ui
from htmltools import tags


@module.ui
def mod_about_ui():
    return ui.nav_panel(
        "About",
        ui.card(
            ui.card_header("About the author"),
            ui.layout_columns(
                ui.div(
                    ui.img(src="author_pic.jpg", width="600px"),
                    class_="d-flex justify-content-center",
                ),
                ui.div(
                    tags.p(
                        """
                        I am a developer and data scientist with a background in
                        bioinformatics and public financial audit. I have always
                        had a keen interest in how tools such as Shiny can help
                        visualise complex data sets. The aim of the LGBFScotland
                        was to create a tool for visualising local government
                        benchmarking framework data that may be of interest to
                        a wide audience. A secondary aim was to provde a
                        platform for my own personal development in creating,
                        maintaining and deploying public Python Shiny applications.
                        """
                    ),
                    tags.p(
                        """
                        I hope you find this application useful. Please feel
                        free to connect with me on linkedin and view my
                        """,
                        tags.a(
                            " personal website ",
                            href="https://jsleight1.github.io/jacksleight.github.io/",
                            target="_blank",
                        ),
                        """
                        which has a copy of my CV and list of other projects I have
                        worked on.
                        """,
                    ),
                    class_="justify-content-center",
                ),
            ),
        ),
        ui.card(
            ui.card_header("About the package"),
            ui.div(
                tags.p(
                    """
                    LGBFScotland is structured as
                    """,
                    tags.a(" uv ", href="https://docs.astral.sh/uv/", target="_blank"),
                    """
                    python package hosted on
                    """,
                    ui.a(
                        " GitHub.",
                        href="https://github.com/jsleight1/lgbfscotland",
                        target="_blank",
                    ),
                ),
                class_="justify-content-center",
            ),
        ),
        ui.card(
            ui.card_header("Disclaimer"),
            tags.h6(
                """
                This python package is licensed using GNU General Public License and contains
                data licensed under the Open Government License (OGL). This application
                is primarily a hobby project, therefore the author accepts no liability and
                provides no guarantees related to the functionality of the application and
                accuracy of the data. The original published data sets should
                always be consulted when using this application.
                """,
                class_="disclaimer",
            ),
        ),
    )
