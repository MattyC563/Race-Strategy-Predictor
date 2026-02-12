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

    # le preparation
    le = le_preperation()
    
    # practice info gatherer
    practice_2_model = practice_analysis([year,gp_name], main_driver, teammate, le)
    
    # previous race info gatherer
    previous_race_model = prev_race_analysis([year,gp_name], prev_main_driver, prev_teammate, le)

    # calibrate last years race data to match the current car
    calibrated_stints = calibration([year, gp_name], main_driver)
    pace_delta = calculate_calibration(practice_2_model, calibrated_stints,le)

    # average temperature calculator
    avg_temp = previous_race_model['avg_track_temp']

    race_strategy_info = race_strategy_creator(previous_race_model, le, event.get_race().total_laps, pace_delta,avg_temp)

    formatter(race_strategy_info)

main()