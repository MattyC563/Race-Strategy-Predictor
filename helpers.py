import fastf1

def last_year_race(track, target_year):
    try:
        event = fastf1.get_event(target_year, track)
        return True
    except Exception:
        return False

def cleaned_laps(laps_data, track):
    fuel_penalty_per_lap = 0.035
    track_evo_per_lap = track_evolution(track)

    # remove in and out laps from pitstops
    clean_laps = laps_data.pick_wo_box()

    # remove any laps not in the dry
    clean_laps = clean_laps[clean_laps['Compound'].isin(['SOFT','MEDIUM','HARD'])]

    # keep laps which were under clear track conditions
    clean_laps = clean_laps.pick_track_status("1")

    # drop any laps where laps aren't valid
    clean_laps = clean_laps.dropna(subset=['LapTime'])

    # apply 107% rule
    clean_laps = clean_laps.pick_quicklaps(1.07)

    # fuel correction
    # convert lap times from time format to seconds
    clean_laps["LapTimeSeconds"] = clean_laps['LapTime'].dt.total_seconds()

    fuel_correction = fuel_penalty_per_lap * clean_laps['LapNumber']
    evo_correction = track_evo_per_lap * clean_laps['LapNumber']

    # add fuel penalty
    clean_laps["FuelCorrectedLapTimes"] = clean_laps["LapTimeSeconds"] + fuel_correction + evo_correction

    return clean_laps

def add_temp(data):
    weather_data = data.get_weather_data()
    data['TrackTemp'] = weather_data['TrackTemp'].values
    return data

def track_evolution(track_name):
    high_evo = ['Monaco','Baku','Las Vegas','Singapore','Miami','Jeddah','Shanghai','Madrid','Mexico']
    medium_evo = ['Melbourne','Montreal','Spa','Monza','Imola','Abu Dhabi','Hungaroring','COTA','Qatar']
    low_evo = ['Bahrain','Silverstone','Suzuka','Barcelona','Zandvoort','Spielberg']

    if track_name in high_evo:
        return -0.025
    elif track_name in medium_evo:
        return -0.015
    elif track_name in low_evo:
        return -0.008
    else:
        return -0.01
    
def delta(prev_race_model, fp2_data, tyre_to_num):
    fp2_cal_data = fp2_data[['TyreLife','Compound','TrackTemp']].copy()
    
    fp2_cal_data['Compound'] = fp2_cal_data['Compound'].map(tyre_to_num)

    prev_model = prev_race_model['model']
    prev_prediction = prev_model.predict(fp2_cal_data)
    fp2_pace = fp2_data['FuelCorrectedLapTimes'].mean()
    pred_prev_pace = prev_prediction.mean()
    pace_delta = fp2_pace - pred_prev_pace

    return pace_delta