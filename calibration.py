import fastf1

def calibration(info, driver):
    fp = fastf1.get_session(info[0], info[1], "FP2")
    fp.load()

    # Filter for driver and remove outliers
    laps = fp.laps.pick_driver(driver).pick_wo_box().pick_quicklaps(1.07)

    # find the longest stint to find most stable race pace
    stints = laps.groupby('Stint').filter(lambda x: len(x) > 5)

    return stints

def calculate_calibration(model, fp_laps, le):
    fp_filtered = fp_laps[['TyreLife','Compound','TrackTemp']].copy()
    fp_filtered['Compound'] = le.transform(fp_filtered['Compound'])

    # Get prediction
    historical_pred = model.predict(fp_filtered)

    # Calculate avg offset
    actual_pace = fp_filtered['LapTime'].dt.total_seconds().mean()
    predicted_pace = historical_pred.mean()

    # adjust for lighter cars in fp2
    pace_delta = actual_pace - predicted_pace + (60 * 0.035)

    return pace_delta