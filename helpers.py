import fastf1

def last_year_race(track, target_year):
    try:
        event = fastf1.get_event(target_year, track)
        return True
    except Exception:
        return False

def cleaned_laps(laps_data):
    fuel_penalty_per_lap = 0.035

    # remove in and out laps from pitstops
    clean_laps = laps_data.pick_wo_box()

    # keep laps which were under clear track conditions
    clean_laps = clean_laps.pick_track_status("1")

    # drop any laps where laps aren't valid
    clean_laps = clean_laps.dropna(subset=['LapTime'])

    # apply 107% rule
    clean_laps = clean_laps.pick_quicklaps(1.07)

    # fuel correction
    # convert lap times from time format to seconds
    clean_laps["LapTimeSeconds"] = clean_laps['LapTime'].dt.total_seconds()

    # add fuel penalty
    clean_laps["FuelCorrectedLapTimes"] = clean_laps["LapTimeSeconds"] + (fuel_penalty_per_lap * clean_laps['LapNumber'])

    return clean_laps

def add_temp(data):
    weather_data = data.get_weather_data()
    data['TrackTemp'] = weather_data['TrackTemp'].values
    return data