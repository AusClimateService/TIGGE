# TIGGE

Download scripts for the [TIGGE](https://confluence.ecmwf.int/display/TIGGE) dataset.

## Storage

The data are downloaded to NCI using the following data reference syntax:
```
/g/data/xv83/TIGGE/data/{model}/{variable}/{type}/{year}/{variable}_6hr_{model}_{type}_{grid}_{YYYYMMDD}.grib
```
For example, perturbed forecast surface temperature (`t2m`) data from the ECMWF forecast model
on a 0.5 degree grid for the Australian region (`AUS`) for a starting date of 25 June 2011
would be archived as follows:

```
/g/data/xv83/TIGGE/data/ECMWF/t2m/perturbed/2011/t2m_6hr_ECMWF_perturbed_AUS-05_20110625.grib
```
