from ecmwfapi import ECMWFDataServer
from calendar import monthrange
from datetime import datetime, timedelta
import argparse

server = ECMWFDataServer()
variable_dict = {
    "t2m": "167",
    "tp": "228228",
    "gh": "156",
}

def parse_time_period(period):
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
            start_date, end_date = parse_time_period(period)
            # Adjust start_date to the specified start_day
            start_date = start_date.replace(day=start_day)
            if start_date > end_date:
                print(f"Start day {start_day} is after the end of the period for {period}. Skipping.")
                continue
        except ValueError as e:
            print(str(e))
            continue
        
        current_date = start_date
        while current_date <= end_date:
            year = current_date.strftime("%Y")
            month = current_date.strftime("%m")
            day = current_date.strftime("%d")

            for variable in variables:
                levtype = "pl" if variable == "gh" else "sfc"
                
                for time in ["00:00:00", "12:00:00"]:
                    for type_val in ["cf", "pf"]:
                        retrieve_dict = {
                            "class": "ti",
                            "dataset": "tigge",
                            "grid": "0.5/0.5",
                            "date": f"{year}-{month}-{day}",
                            "expver": "prod",
                            "levtype": levtype,
                            "origin": "ecmf",
                            "param": variable_dict[variable],
                            "step": "/".join(str(i) for i in range(0, 361, 6)),
                            "number": "/".join(str(i) for i in range(1, 51)),
                            "time": time,
                            "type": type_val,
                            "target": f"/g/data/xv83/TIGGE/data/ECMWF/{variable}/{type_val}/{year}/{month}/{time[:2]+time[3:5]}/{variable}_6hr_ECMWF_{type_val}_GLO-05_{year}{month}{day}.grib"
                        }
                        
                        if variable == "gh":
                            retrieve_dict["levelist"] = "500"
                        
                        try:
                            # print(retrieve_dict)
                            server.retrieve(retrieve_dict)
                        except Exception as e:
                            print(f"Error retrieving data for {year}-{month}-{day}, {variable}, {time}: {str(e)}")
            
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
