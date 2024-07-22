# TIGGE

This project provides download scripts for the [TIGGE](https://confluence.ecmwf.int/display/TIGGE) data from the ECMWF server. It allows users to retrieve and download forecasts for specific time periods and variables. 

## Requirements

Before you execute the script, you will need to do the following;

__Sign up and retrieve your key:__
  1. Visit ECMWF's [TIGGE portal](http://apps.ecmwf.int/datasets/data/tigge)
  2. Click "login" in "Please login before retrieving data from this dataserver" to complete a user registration
  3. After you log in, retrieve your key at https://api.ecmwf.int/v1/key/
  4. Create a .ecmwfapirc file in your $HOME directory using ```nano .ecmwfapirc```, and paste the the key information into it. It should look something like:
  ```
  {
    "url"   : "https://api.ecmwf.int/v1",
    "key"   : "YOUR_API_KEY",
    "email" : "your.email@example.com"
  }
  ```
       

__Install the ECMWF client:__  
  The client is already installed in the analysis3-24.04 module on hh5. If you would like to add it to your own environment instead, do so with ```python3 -m pip install -v --no-binary :all: ecmwf-api-client```



## Usage

The .py script can be run from the command line with: 
```
python TIGGE_data_retrieval.py <time periods>... <variables>... [--start_day START DAY]
```
__Parameters:__
* ```time_periods```: List of time periods in YYYY or YYYY-MM format
* ```variables```: List of variables to retrieve. Options are:
  * ```t2m```: 2 meter temperature
  * ```tp```: Total precipitation
  * ```gh```: Geopotential height at 500hPa
* start_day: The day of the month to start retrieval from. This is optional (default is 1). I have included this as sometimes a month doesn't get the chance to fully download, and it can be useful to start from a particular day. 

Example requests:
```
python TIGGE_data_retrieval.py 2007 2008 t2m tp gh

python TIGGE_data_retrieval.py 2007-01 gh --start_day=5
```

## Storage

The data are downloaded to NCI using the following data reference syntax:
```
/g/data/xv83/TIGGE/data/{model}/{variable}/{type}/{year}/{month}/{time}/{variable}_6hr_{model}_{type}_{grid}_{YYYYMMDD}.grib
```
For example, perturbed forecast (`pf`) surface temperature (`t2m`) data from the ECMWF forecast model
on a 0.5 degree grid for the Australian region (`AUS`) for a starting date of 25 June 2011 and start time 0000
would be archived as follows:

```
/g/data/xv83/TIGGE/data/ECMWF/t2m/pf/2011/06/0000/t2m_6hr_ECMWF_pf_GLO-05_20110625.grib
```
