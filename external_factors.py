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

def calculate_race_probabilities(track):
    # get the years that this event occurred in
    years_occurred = year_finder(track)

    if years_occurred == []:
        return [0.5,0.5,0.5]
    
    return_data = []
    for year in years_occurred:
        session = fastf1.get_session(year, track, "R")
        sc = event_finder(session, "4")
        vsc = event_finder(session, "6")
        red_flag = event_finder(session, "")


def year_finder(track):
    years_occurred = []
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
    pass