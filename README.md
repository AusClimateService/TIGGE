# TIGGE

This project provides download scripts for the [TIGGE](https://confluence.ecmwf.int/display/TIGGE) data from the ECMWF server. Specifically, the scripts are designed to retrieve data for the ECMWF forecast model, though this could be adapted for other models without too much hassle. It allows users to download forecasts for specific time periods and variables.

*__NOTE__: Public access to this dataset will be transitioning to a new interface, with dates to be announced soon. This may impact this retrieval method. On the ECMWF website they direct you [here](https://confluence.ecmwf.int/display/DAC/Decommissioning+of+ECMWF+Public+Datasets+Service) for more information on how to access this data in the future.*

## Contents
1. `TIGGE_data_retrival.py`: A Python script which can be run from the command line to download TIGGE data.
2. `TIGGE_copyq_job.sh`: A shell script for submitting a job to the NCI copyq queue.
3. `TIGGE_copyq_job.py`: A Python script executed by the shell script.

The copyq files accomplish the same thing as `TIGGE_data_retrival.py` - I have just provided alternative options based on the preference of the user. 

## ECMWF TIGGE Data Parameters

This tool retrieves data from the ECMWF model with the following specifications:

#### Forecast Types
- Control Forecast (cf): 1 ensemble member
- Perturbed Forecast (pf): 50 ensemble members

#### Initialization Times
- 00:00:00 UTC
- 12:00:00 UTC

#### Forecast Length
- Total forecast length: 360 hours (15 days)
- Time step: 6 hours

#### Spatial Resolution
- Grid: 0.5° x 0.5° (global)

#### Variables Available
- 2-meter Temperature (t2m)
- Total Precipitation (tp)
- Geopotential Height at 500 hPa (gh)

#### Data Range
- Available data spans from October 2006 to present day

#### Data Format
- Output format: GRIB

## Requirements

Before you execute the either of the scripts, you will need to do the following;

__Sign up and retrieve your key:__
  1. Visit ECMWF's [TIGGE portal](http://apps.ecmwf.int/datasets/data/tigge)
  2. Click "login" in "Please login before retrieving data from this dataserver" to complete a user registration
  3. After you log in, retrieve your key at https://api.ecmwf.int/v1/key/
  4. Create a .ecmwfapirc file in your $HOME directory using ```nano .ecmwfapirc```, and paste the key information into it. It should look something like:
  ```
  {
    "url"   : "https://api.ecmwf.int/v1",
    "key"   : "XXXXXXXXXXXXXXXXXXX",
    "email" : "your.email@example.com"
  }
  ```

## Usage

### Option 1: Executing the Python Script from the Command Line
First, load a module that has the ECMWF API client. Currently the module analysis3-24.04 on hh5 has it installed. Load the module with:
  ```
  module use /g/data/hh5/public/modules
  module load conda/analysis3-24.04
```
Ensuring you are in the directory with `TIGGE_data_retrieval.py` in it, run the script from the command line with: 
```
python TIGGE_data_retrieval.py <time_periods>... <variables>... [--start_day START_DAY]
```
__Parameters:__
* ```<time_periods>```: One or more time periods in YYYY or YYYY-MM format
* ```<variables>```: One or more variables to retrieve. Options are:
  * ```t2m```: 2 meter temperature
  * ```tp```: Total precipitation
  * ```gh```: Geopotential height at 500hPa
* ```--start_day START_DAY```: (Optional) Day of the month to start retrieval (default is 1). This is included as sometimes a month doesn't get the chance to fully download, and it can be useful to start from a particular day. 

Example requests:
```
python TIGGE_data_retrieval.py 2007 2008 t2m tp gh

python TIGGE_data_retrieval.py 2007-01 gh --start_day 5
```
The script is designed to send off a request one day at a time, iterating through a loop until it reaches the desired time span. It first fetches the single control forecast, then the perturbed forecast file with all 50 ensemble members. For this reason, you will find that every second download will take significantly longer, and thus will sit at "Request is active" for a while. 

### Option 2: Submitting an NCI CopyQ Job

To submit a job to the NCI copyq queue:

1. Check you have access to the required projects (xv83, hh5).
2. Make sure `TIGGE_copyq_job.py` contains the desired data retrieval parameters. There is a section at the top of the script to edit.
3. Ensuring you are in the directory containing both the .py and .sh files, submit the job using the following command:
```
qsub TIGGE_copyq_job.sh
```
This will execute `TIGGE_copyq_job.py` in the copyq queue with the specified resources. Note that the maximum walltime for the copyq queue is 10 hours. Once the job has completed/reached its maximum time allowance, it will return an output file and error report in the same directory as the files. You can check on your job status with `qstat`. 

### Extra Info

Due to ECMWF's restrictions, you are only allowed to submit one request at a time per account. If multiple requests are submitted they will enter a queue. You can view and manage your active and queued requests [here](https://apps.ecmwf.int/webmars/joblist/).


## Storage

The data are downloaded to NCI using the following data reference syntax:
```
/g/data/xv83/TIGGE/data/{model}/{variable}/{type}/{year}/{month}/{time}/{variable}_6hr_{model}_{type}_{grid}_{YYYYMMDD}.grib
```
For example, perturbed forecast (`pf`) surface temperature (`t2m`) data from the ECMWF forecast model
on a 0.5 degree grid for the global region (`GLO`) for a starting date of 25 June 2011 and start time of 00:00:00
would be archived as follows:

```
/g/data/xv83/TIGGE/data/ECMWF/t2m/pf/2011/06/0000/t2m_6hr_ECMWF_pf_GLO-05_20110625.grib
```
