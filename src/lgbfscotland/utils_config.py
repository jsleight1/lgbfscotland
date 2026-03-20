from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[".secrets.toml"],
    environments=True,
    load_dotenv=True,
)
