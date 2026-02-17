# imports from other files
from helpers import *
from analysis import *

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

    print("All successful so far!\n" + str(fp2_model) + "\n" + str(prev_race_model))

    # calculate pit loss time

    # calculate rough track evolution (0.01s/lap)

    # allow the user to input guesses for possible tyre strategies, which the model can check

    # use the models to roughly find the best strategy with least total time

    # output strategy cleanly

    # create a graph to show all the different strategies using matplotlib
main()