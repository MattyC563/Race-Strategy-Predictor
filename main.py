# imports from other files
from helpers import *
from analysis import *
from external_factors import *
from creator import *

# imports from other libraries
import fastf1
import logging

def main():
    # disable logging 
    logging.disable(logging.INFO)

    # basic information gathering
    print("Welcome to my race strategy program.")
    year = int(input("Please input the year of the race you want to predict:\n"))
    track_name = str(input("Please input the name of the circuit you are racing at:\n"))
    main_driver = str(input("Please input the abbreviation for your driver:\n")).upper()

    # identify whether the race occurred last year
    if last_year_race(track_name, year-1):
        prev_driver = str(input("Input the abbreviation of the driver who drove for you last year:\n")).upper()
        prev_race = True
    else:
        prev_race = False

    # load the race weekends for fp2 and last year's race, and cleans them
    # cleans laps by removing outlaps, inlaps, laps with events along with adjusting for fuel consumption
    fp2_data = fastf1.get_session(year, track_name, "FP2")
    fp2_data.load()
    fp2_data = cleaned_laps(fp2_data.laps.pick_driver(main_driver))

    if prev_race:
        prev_race_data = fastf1.get_session(year, track_name, "R")
        prev_race_data.load()
        prev_race_pitstops = prev_race_data.copy()
        prev_race_data = cleaned_laps(prev_race_data.laps.pick_driver(prev_driver))

    # add necessary weather data to datasets
    fp2_data = add_temp(fp2_data)
    prev_race_data = add_temp(prev_race_data)

    # prepare the LabelEncoder for model making
    le = le_preparation()

    # make the models for fp2 and previous race
    fp2_model = stint_analysis(fp2_data, le)
    if prev_race:
        prev_race_model = stint_analysis(prev_race_data, le)

    # CALCULATE TRACK EVOLUTION

    # CALCULATE AVG TEMP

    # CALCULATE EXPECTED DELTA

    # calibrate the previous race model for a better car
    # DO THIS

    # combine all data into one big model
    model = ""

    # calculate pit loss time
    if prev_race:
        pit_loss_time = pit_lane_time(prev_race_pitstops, prev_driver)

    # calculate probabilities of safety cars, vscs, red flags
    event_probabilities = calculate_event_probabilities(track_name)

    # set all strategies that the model can check
    # 1 = medium, 2 = softs, 0 = hards
    poss_strategies = [[2,1],[2,0],[0,1],[2,2,1],[2,2,0],[1,1,0],[1,1,2]]

    # find more information for final strategy
    total_laps = 0

    # use the models to roughly find the best strategy with least total time
    # final_outcome = race_strategy_creator(model, le, total_laps, pace_delta, avg_temp, pit_loss_time, track_evo, fuel_burn=0.035)

    # output strategy cleanly

    # create a graph to show all the different strategies using matplotlib
main()