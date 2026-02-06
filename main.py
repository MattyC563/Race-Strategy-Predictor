# imports for clean_data
import fastf1
import logging
import pandas as pd

# imports for data_analysis
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# imports for displaying data
import matplotlib.pyplot as plt
import numpy as np

def main():
    # disable logging 
    logging.disable(logging.INFO)

    # basic information gathering
    print("Welcome to my race strategy program.")
    year = int(input("Please input the year of the race you want to predict:\n"))
    gp_name = str(input("Please input the name of the race you want to predict:\n"))

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
    
    # practice info gatherer
    practice_total_info = {}
    for i in range(1, no_of_practice+1):
        practice_total_info[f"FP{i}"] = practice_analysis([year,gp_name], i)
    
    # previous race info gatherer
    previous_race_info = prev_race_analysis([year,gp_name])

    race_strategy_info = race_strategy_creator(practice_total_info, previous_race_info)

    formatter(race_strategy_info)

def practice_analysis(info, practice_no):
    practice_s = fastf1.get_session(info[0],info[1],f"FP{practice_no}")

def prev_race_analysis(info):
    race = fastf1.get_session(info[0],info[1],"R")

def race_strategy_creator(previous_info, practice_info):
    pass

def formatter(info):
    pass

main()