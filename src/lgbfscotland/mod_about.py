from shiny import module, ui
from htmltools import tags


@module.ui
def mod_about_ui():
    """
    Title
    -----
    About module UI
    """
    return ui.nav_panel(
        "About",
        ui.div(
            ui.card(
                ui.card_header("About the author"),
                ui.layout_columns(
                    ui.div(
                        ui.img(src="author_pic.jpg", width="400px"),
                        class_="d-flex justify-content-center",
                    ),
                    ui.div(
                        tags.p(
                            """
                            I am a data scientist and software developer with a
                            background in bioinformatics and public audit. I
                            have always had a keen interest in how tools such as
                            Shiny can help visualise complex data sets. The aim
                            of the LGBFScotland was to create a tool for
                            visualising local government benchmarking framework
                            data. A secondary aim was to provde a platform for
                            my own personal development in creating, maintaining
                            and deploying public Python Shiny applications.
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
                            which has a copy of my CV and a list of other projects I
                            have worked on.
                            """,
                        ),
                        class_="justify-content-center",
                    ),
                ),
                min_height="350px",
            ),
            ui.card(
                ui.card_header("About the package"),
                ui.div(
                    tags.p(
                        """
                        LGBFScotland is structured as
                        """,
                        tags.a(
                            " uv ", href="https://docs.astral.sh/uv/", target="_blank"
                        ),
                        """
                        python package hosted on
                        """,
                        ui.a(
                            " GitHub.",
                            href="https://github.com/jsleight1/lgbfscotland",
                            target="_blank",
                        ),
                        """
                        This application is deployed using the Azure container app
                        platform which uses a docker container that is published on
                        """,
                        tags.a(
                            " docker.io",
                            href="https://hub.docker.com/r/jsleight1/lgbfscotland/",
                            target="_blank",
                        ),
                        ".",
                    ),
                    tags.p(
                        """
                        All data used in this application is available from the
                        Local Government Benchmarking Framework
                        """,
                        tags.a(
                            "(LGBF)",
                            href="https://www.improvementservice.org.uk/benchmarking/home",
                            target="_blank",
                        ),
                        """
                        . Specifically the 'LGBF indicators information' and
                        'LGBF Data Table Real' data sets were downloaded from
                        the
                        """,
                        tags.a(
                            "Spatial Hub",
                            href="https://data.spatialhub.scot/dataset/local_government_benchmarking_framework-is",
                            target="_blank",
                        ),
                        """
                        . These data sets are licensed under a UK Open Government
                        Licence (OGL) license.
                        """,
                    ),
                    class_="justify-content-center",
                ),
                min_height="200px",
            ),
            ui.card(
                ui.card_header("Disclaimer"),
                tags.h6(
                    """
                    This python package is licensed using GNU General Public
                    License and contains data licensed under the UK Open
                    Government License (OGL). This application is primarily a
                    hobby project, therefore the author accepts no liability and
                    provides no guarantees related to the functionality of the
                    application and accuracy of the data. The original published
                    data sets should always be consulted when using this
                    application.
                    """,
                    class_="disclaimer",
                ),
                min_height="150px",
            ),
            class_="overflow-auto",
            style="height: 100%;",
        ),
    )
