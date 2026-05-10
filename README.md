# lgbfscotland

<!-- badges: start -->
[![Test](https://github.com/jsleight1/lgbfscotland/actions/workflows/test.yml/badge.svg)](https://github.com/jsleight1/lgbfscotland/actions/workflows/test.yml)
<!-- badges: end -->

This repository contains a Python package for the <a
href="https://www.lgbfscotland.co.uk/" target="_blank">lgbfscotland</a>  shiny
application. This shiny application downloads, processes and presents local
government benchmarking framework (LGBF) data.

# Installation

`lgbfscotland` is structured as a [uv](https://docs.astral.sh/uv/) package and
can be installed by cloning the repo and performing the following:

```
pip install uv
uv sync
```

# Usage

`lgbfscotland` using `Dynaconf` to separate usage in development and production
envrionments. To run the app locally a `.env` file must be created as follows:

```
ENV_FOR_DYNACONF="development"
```

The next step is to download the processed LGBF data. This can be done within a
python session.

```
from lgbfscotland.utils_data_processing.py import save_lgbf_data
save_lgbf_data()
```

This will save the LGBF as a parquet file. The shiny app can then by run locally from your terminal.

```
uv run shiny run app.py
```

Alternatively a dockerised version of the application is available from
[docker.io](https://hub.docker.com/r/jsleight1/lgbfscotland).

This can be launched by using:

```
docker run -p 9003:9003 -it docker.io/jsleight1/lgbfscotland:latest
```

The application can then be viewed at:

```
http://localhost:9003/
```

## Disclaimer

This python package is licensed using GNU General Public License and contains
data licensed under the UK Open Government License (OGL). This application is
primarily a hobby project, therefore the author accepts no liability and
provides no guarantees related to the functionality of the application and
accuracy of the data. The original published data sets should always be
consulted when using this application.
