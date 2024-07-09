from ecmwfapi import ECMWFDataServer
import sys
from calendar import monthrange

server = ECMWFDataServer()

VAR_PARAM_NUMBER = {
                    "t2m" : "167", 
                    "tp" : "228228",
                    "gh" : "156",
}

def data_retriever(year, variable):

    """
    Retrieves TIGGE data for a given year and variable from ECMWF for both control and perturbed forecasts. 
    The gridding size is the default 0.5/0.5.
    The area is N/W/S/E = 0/90/-55/180 (Australia region).

    Args:
        year (str): Year in YYYY format
        variable (str): Variable  to retrieve data for. Options are:
           - t2m: 2 meter temperature
           - tp: Total precipitation
           - gh: Geopotential height at 500hPa

    Returns: 
        None. Saves .grib files for each day, for both perturbed and control forecasts. 
        The files will be saved to /g/data/xv83/TIGGE/data/ECMWF

    """

    levtype = "pl" if variable == "gh" else "sfc"
    
    for month in range(1, 13):
        _, days_in_month = monthrange(int(year), month)
        month_str = f"{month:02d}"
        
        for day in range(1, days_in_month + 1):
            day_str = f"{day:02d}"
            
            for type_val in ["cf", "pf"]:
                retrieve_dict = {
                    "class": "ti",
                    "dataset": "tigge",
                    "date": f"{year}-{month_str}-{day_str}",
                    "expver": "prod",
                    "grid": "0.5/0.5",
                    "area": "0/90/-50/180",
                    "levtype": levtype,
                    "origin": "ecmf",
                    "param": VAR_PARAM_NUMBER[variable],
                    "step": "/".join(str(i) for i in range(0, 361, 6)),
                    "time": "00:00:00/12:00:00",
                    "type": type_val,
                    "target": f"/g/data/xv83/TIGGE/data/ECMWF/{variable}/{type_val}/{year}/{month_str}/{variable}_6hr_ECMWF_{type_val}_AUS-05_{variable}_{year}{month_str}{day_str}.grib"
                }
                
                if variable == "gh":
                    retrieve_dict["levelist"] = "500"
                if type_val == "pf":
                    retrieve_dict["number"] = "/".join(str(i) for i in range(1, 51))
    
                server.retrieve(retrieve_dict)
        


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <year> <variable>")
        sys.exit(1)
    
    year = sys.argv[1]
    variable = sys.argv[2]

data_retriever(year, variable)