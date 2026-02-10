# function imports
from analysis import *
from creator import *
from formatter import *
from calibration import *

# imports for clean_data
import fastf1
import logging

def main():
    # disable logging 
    logging.disable(logging.INFO)

    # basic information gathering
    print("Welcome to my race strategy program.")
    year = int(input("Please input the year of the race you want to predict:\n"))
    gp_name = str(input("Please input the name of the race you want to predict:\n"))
    
    main_driver = str(input("Please input the abbreviation for your driver:\n")).upper()
    teammate = str(input("Please input the abbreviation for your driver's teammate:\n")).upper()

    prev_race = str(input("Did this race occur last year? (y/n)")).lower()
    if prev_race == "y":
        prev_main_driver = str(input("Please input the abbreviation for your main driver from the previous year's race:\n")).upper()
        prev_teammate = str(input("Please input the abbreviation for your main driver from last year's teammate:\n")).upper()

    # load race weekend
    event = fastf1.get_event(year, gp_name)

    # gather key information
    # number of practice sessions
    sessions = [event['Session1'], event['Session2'], event['Session3'], 
            event['Session4'], event['Session5']]
    no_of_practice = sum(1 for s in sessions if "Practice" in str(s))

    # load race from previous year
    try:
        prev_event = fastf1.get_event(year-1, gp_name)
    except ValueError:
        print("This event didn't occur in the previous year.")

    # le preparation
    le = le_preperation()
    
    # practice info gatherer
    practice_total_info = {}
    for i in range(1, no_of_practice+1):
        practice_total_info[f"FP{i}"] = practice_analysis([year,gp_name], i, main_driver, teammate, le)
    
    # previous race info gatherer
    previous_race_info = prev_race_analysis([year,gp_name], prev_main_driver, prev_teammate, le)

    # calibrate last years race data to match the current car
    calibrated_stints = calibration([year, gp_name], main_driver)
    pace_delta = calculate_calibration(practice_total_info["FP2"],calibrated_stints,le)

    race_strategy_info = race_strategy_creator(practice_total_info, previous_race_info)

    formatter(race_strategy_info)

main()