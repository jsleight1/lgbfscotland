import requests
import io
import os
import pandas as pd
from dynaconf import LazySettings
from lgbfscotland.utils_config import settings
from azure.storage.blob import BlobServiceClient, BlobClient
from typing import Dict


def _lgbf_metadata_url() -> str:
    return "https://data.spatialhub.scot/dataset/9a3728b4-49ea-40af-ab10-fc0305bace84/resource/00845629-44d0-489e-8c5e-9f49ed6b19ce/download/indicator-information.csv"


def _lgbf_data_url() -> str:
    return "https://data.spatialhub.scot/dataset/9a3728b4-49ea-40af-ab10-fc0305bace84/resource/7ba35197-7ca7-4477-a38b-01fd4180466b/download/lgbf_data_table_real.csv"


def process_lgbf_data(
    metadata_url: str = _lgbf_metadata_url(), data_url: str = _lgbf_data_url()
) -> pd.DataFrame:
    """
    Title
    -----
    Process LGBF data into useable format by lgbfscotland application

    Parameters
    ----------
    metadata_url: str
        URL for lgbf metadata in spatial hub.
    data_url: str
        URL for lgbf data in spatial hub
    """
    metadata_cols = _required_lgbf_metadata_cols()
    metadata = _read_bytes_csv(metadata_url).rename(columns=metadata_cols)[
        metadata_cols.values()
    ]
    data = _read_bytes_csv(data_url)
    output = data.merge(metadata, on="Indicators_Information_Code", how="inner")
    return output


def _read_bytes_csv(x: str) -> pd.DataFrame:
    req = requests.get(x)
    req.raise_for_status()
    return pd.read_csv(io.BytesIO(req.content))


def _required_lgbf_metadata_cols() -> Dict[str, str]:
    return {
        "Code": "Indicators_Information_Code",
        "Title": "Indicators_Information_Title",
        "ServiceArea": "Indicators_Information_ServiceArea",
        "Numerator_Title": "Indicators_Information_Numerator_Title",
        "Denominator_Title": "Indicators_Information_Denominator_Title",
        "Unit": "Indicators_Information_Unit",
        "Category": "Indicators_Information_Category",
    }


def save_lgbf_data(settings: LazySettings = settings, **kwargs) -> bool:
    """
    Title
    -----
    Save processed LGBF data into useable format by lgbfscotland application
    as either local or azure remote parquet file.

    Parameters
    ----------
    settings: LazySettings
        Settings config loaded from settings.toml
    **kwargs: Any
        Additional key arguments passed to _save_local_lgbf_data and _save_azure_lgbf_data
    """
    match settings.type:
        case "development":
            return _save_local_lgbf_data(**kwargs)
        case "production":
            return _save_azure_lgbf_data(**kwargs)


def _save_local_lgbf_data(
    settings: LazySettings = settings,
    data: pd.DataFrame = process_lgbf_data(),
    **kwargs,
) -> bool:
    data.to_parquet(path=settings.processed_data_file, engine="pyarrow")
    return os.path.exists(settings.processed_data_file)


def _save_azure_lgbf_data(
    settings: LazySettings = settings,
    data: pd.DataFrame = process_lgbf_data(),
    **kwargs,
) -> bool:
    parquet_buffer = io.BytesIO()
    data.to_parquet(parquet_buffer, engine="pyarrow")
    parquet_buffer.seek(0)
    blob_client = get_blob_client(settings=settings)
    blob_client.upload_blob(parquet_buffer, overwrite=True)
    return blob_client.exists()


def load_lgbf_data(settings: LazySettings = settings, **kwargs) -> pd.DataFrame:
    """
    Title
    -----
    Load processed LGBF data for use by lgbfscotland application
    from either local or azure remote parquet file.

    Parameters
    ----------
    settings: LazySettings
        Settings config loaded from settings.toml
    **kwargs: Any
        Additional key arguments passed to _load_local_lgbf_data and _load_azure_lgbf_data
    """
    match settings.type:
        case "development":
            output = _load_local_lgbf_data(settings=settings, **kwargs)
        case "production":
            output = _load_azure_lgbf_data(settings=settings, **kwargs)
    return output


def _load_local_lgbf_data(settings: LazySettings = settings, **kwargs) -> pd.DataFrame:
    return pd.read_parquet(settings.processed_data_file)


def _load_azure_lgbf_data(settings: LazySettings = settings, **kwargs) -> pd.DataFrame:
    blob_client = _get_blob_client(settings=settings)
    assert blob_client.exists(), "Data file doesn't exist in blob"
    download_stream = blob_client.download_blob()
    blob_data = io.BytesIO(download_stream.readall())
    output = pd.read_parquet(blob_data, engine="pyarrow")
    return output


def _get_blob_client(settings: LazySettings = settings) -> BlobClient:
    blob_service_client = BlobServiceClient(
        settings.blob_account_url, credential=settings.blob_account_key
    )
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_STORAGE_CONTAINER, blob=settings.processed_data_file
    )
    return blob_client
