import sys
import datetime

def validation_input(date_input):
    try:
        datetime.datetime.strptime(date_input,"%Y%m%d")
    except ValueError:
        raise ValueError("Input parameter should YYYYMMDD")
        sys.exit(1)