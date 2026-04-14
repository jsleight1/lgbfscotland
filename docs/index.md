# lgbfscotland

This repository contains a Python package for the `lgbfscotland' shiny application. This shiny application downloads, processes and presents
local government benchmarking framework (LGBF) data.

# Installation

[lgbfscotland](www.lgbfscotland.co.uk) is structured as a [uv](https://docs.astral.sh/uv/) package and can be installed by cloning the repo and performing
the following:

```
pip install uv
uv sync
```

# Usage

`lgbfscotland` using `Dynaconf` to separate usage in development and
production envrionments. To run the app locally a `.env` file must be
created as follows:

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

