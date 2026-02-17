import statistics
import fastf1

# Fixed version of your existing function
def pit_lane_time(session, driver):
    session.load(laps=True)
    driver_laps = session.laps.pick_driver(driver)
    pit_stop_laps = driver_laps.pick_box_laps()
    
    avg_counter = []
    for index, lap in pit_stop_laps.iterrows():
        # Added .total_seconds() and fixed PitInTime
        time_in_pits = (lap['PitOutTime'] - lap['PitInTime']).total_seconds()
        avg_counter.append(time_in_pits)
        
    return statistics.fmean(avg_counter)

def calculate_event_probabilities(track):
    # get the years that this event occurred in
    years_occurred = year_finder(track)

    # if race hasn't occurred before, presume that it is equally like and unlikely for a safety car
    if years_occurred == []:
        return [0.5,0.5,0.5]
    
    # iterate through each year, determine whether any events occurred
    return_data = {'SC': 0, 'VSC':0, 'red_flag':0}
    for year in years_occurred:
        session = fastf1.get_session(year, track, "R")
        return_data['SC'] += event_finder(session, "4")
        return_data['VSC'] += event_finder(session, "6")
        return_data['red_flag'] += event_finder(session, "5")

    # find rough probability of events occurring
    for num in return_data.keys:
        num = num / len(years_occurred)

    return return_data


def year_finder(track):
    years_occurred = []

    # iterate through all events in the possible timespan for fastf1
    for year in range(2018,2025):
        try:
            schedule = fastf1.get_event_schedule(year)
            matches = schedule[schedule['EventNumber'].str.contains(track, case=False, na=False)]
            if not matches.empty:
                years_occurred.append(year)

        except Exception:
            continue
    
    return years_occurred

def event_finder(session, event_num):
    session.load()
    laps = session.laps.pick_track_status(event_num)
    # returns 1 rather than number of events because we are finding probabilities with this
    if laps.empty:
        return 0
    else:
        return 1