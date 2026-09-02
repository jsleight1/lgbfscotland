## Introduction

## Data sources

The data sets used by the application are sourced from the Local Government
Benchmarking Framework
([LGBF](https://www.improvementservice.org.uk/benchmarking/)) using the [Spatial
Hub](https://data.spatialhub.scot/dataset/local_government_benchmarking_framework-is). These data sets are licensed under a UK Open Government Licence (OGL) license.

## Data workflow

The 'LGBF indicators information' and 'LGBF Data Table Real' data sets are
obtained periodically using a GitHub action and manipulated into a single data
set. This data workflow creates a single parquet file which are stored as  in an
Azure blob. This Azure blob is accessed when the shiny application launches. The
data set is periodically updated every 6 months using a GitHub action.