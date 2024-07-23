from ecmwfapi import ECMWFDataServer
from calendar import monthrange
from datetime import datetime, timedelta
import argparse

# Initialise the ECMWF Data server
server = ECMWFDataServer()

# Dictionary mapping variable names to their ECMWF codes (for later use)
variable_dict = {
    "t2m": "167", # 2 meter temp
    "tp": "228228", # Total precipitation
    "gh": "156", # Geopotential height at 500hPa
}


def parse_time_period(period):
    """
    Parse a time period string into start and end dates.
    Args: 
        period (str): Time period in YYYY or YYYY-MM format
    Returns:
        tuple: (start_date, end_date) as datetime objects
    """
    
    if len(period) == 4:  # YYYY format
        return datetime(int(period), 1, 1), datetime(int(period), 12, 31)
    elif len(period) == 7:  # YYYY-MM format
        year, month = map(int, period.split('-'))
        _, last_day = monthrange(year, month) 
        return datetime(year, month, 1), datetime(year, month, last_day)
    else:
        raise ValueError(f"Invalid time period format: {period}")

def data_retriever(time_periods, variables, start_day=1):
    """
    Retrieves TIGGE data for given time periods and variables from ECMWF for both control and perturbed forecasts. 
    The gridding size is the default 0.5/0.5.
    The area is global.
    
    Args:
        time_periods (list): List of time periods in YYYY or YYYY-MM format
        variables (list): List of variables to retrieve data for. Options are:
           - t2m: 2 meter temperature
           - tp: Total precipitation
           - gh: Geopotential height at 500hPa
        start_day (int): The day of the month to start from (default is 1)
           
    Returns: 
        None. Saves .grib files for each day, for both perturbed and control forecasts. 
        The files will be saved to /g/data/xv83/TIGGE/data/ECMWF
    """
    
    for period in time_periods:
        try:
            # Retrieve the start and end dates for the given time period
            start_date, end_date = parse_time_period(period)
            
            # Adjust start date to the specified start_day
            start_date = start_date.replace(day=start_day)
            if start_date > end_date:
                print(f"Start day {start_day} is after the end of the period for {period}. Skipping.")
                continue
        except ValueError as e:
            print(str(e))
            continue
        
        current_date = start_date
        
        # Run loop for all days within the time period
        while current_date <= end_date:
            year = current_date.strftime("%Y")
            month = current_date.strftime("%m")
            day = current_date.strftime("%d")

            # Loop through variables (if multiple were given)
            for variable in variables:
                # Set level type (either pressure level or surface level) based on the chosen variable
                levtype = "pl" if variable == "gh" else "sfc"
                
                # Loop through the 2 initialisation times
                for time in ["00:00:00", "12:00:00"]:
                    
                    # Loop through forecast types
                    for type_val in ["cf", "pf"]:

                        # Prepare retrieval dictionary with ECMWF API parameters.
                        retrieve_dict = {
                            "class": "ti",                    
                            "dataset": "tigge",
                            "expver": "prod",
                            "grid": "0.5/0.5",                # Grid interval in degrees (e.g. 1/1, 2.5/2.5, N160, T319)
                            "date": f"{year}-{month}-{day}",  # Date in DD-MM-YYYY format. Can retrieve multiple days with 01/01/2024/to/03/01/2024 for example
                            "levtype": levtype,               # Pressure level (pl) or surface level (sfc)
                            "origin": "ecmf",                 # NWP centre (e.g. all, bom, cma, ecmwf etc.)   
                            "param": variable_dict[variable], # Variable (e.g. gh, t2m)
                            "step": "/".join(str(i) for i in range(0, 361, 6)),  # Forecast lead times (e.g. 6/12/18/24/36). In 6-hour steps for ecmwf
                            "number": "/".join(str(i) for i in range(1, 51)),    # Ensemble member numbers. 1 for cf, 50 for pf. 
                            "time": time,                     # Initialisation times (e.g. 00:00:00 or 12:00:00) 
                            "type": type_val,                 # Forecast type (e.g. pf or cf)
                            # File directory and name
                            "target": f"/g/data/xv83/TIGGE/data/ECMWF/{variable}/{type_val}/{year}/{month}/{time[:2]+time[3:5]}/{variable}_6hr_ECMWF_{type_val}_GLO-05_{year}{month}{day}.grib"
                        }

                        # Add an additional entry to the dictionary if geopotential height is the chosen variable
                        if variable == "gh":
                            retrieve_dict["levelist"] = "500"   # Other options are 1000, 925, 850, 700, 500, 300, 250 and 200
                        
                        try:
                            # Retrieve data using the ecmwfapi function, feeding in our dictionary
                            server.retrieve(retrieve_dict)
                        except Exception as e:
                            print(f"Error retrieving data for {year}-{month}-{day}, {variable}, {time}: {str(e)}")
                            
            # Move to next day
            current_date += timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description='Retrieve ECMWF TIGGE data.')
    parser.add_argument('time_periods', nargs='+', help='Time periods in YYYY or YYYY-MM format')
    parser.add_argument('variables', nargs='+', choices=['t2m', 'tp', 'gh'], help='Variables to retrieve')
    parser.add_argument('--start_day', type=int, default=1, help='Day of the month to start retrieval')
    
    args = parser.parse_args()
    
    data_retriever(args.time_periods, args.variables, start_day=args.start_day)

if __name__ == '__main__':
    main()
