# TIGGE

Download scripts for the [TIGGE](https://confluence.ecmwf.int/display/TIGGE) dataset.

## Usage

The .py script can be run from the command line with: 
```
python TIGGE_data_retrieval.py <year> <variable>
```
The packages ecmwf-api-client and calendar are required. 

## Storage

The data are downloaded to NCI using the following data reference syntax:
```
/g/data/xv83/TIGGE/data/{model}/{variable}/{type}/{year}/{month}/{variable}_6hr_{model}_{type}_{grid}_{YYYYMMDD}.grib
```
For example, perturbed forecast (`pf`) surface temperature (`t2m`) data from the ECMWF forecast model
on a 0.5 degree grid for the Australian region (`AUS`) for a starting date of 25 June 2011
would be archived as follows:

```
/g/data/xv83/TIGGE/data/ECMWF/t2m/pf/2011/06/t2m_6hr_ECMWF_perturbed_AUS-05_20110625.grib
```
