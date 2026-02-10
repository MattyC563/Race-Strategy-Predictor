# imports
import fastf1
import logging

# imports for data_analysis
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def practice_analysis(info, practice_no, main_driver, teammate, le):
    # load the specific session
    practice_s = fastf1.get_session(info[0],info[1],f"FP{practice_no}")
    practice_s.load()

    # create a column for laps since start of the stint 'LapsInStint'
    main_laps = practice_s.laps.pick_driver(main_driver)
    main_laps['LapsInStint'] = main_laps.groupby('Stint').cumcount() + 1

    other_laps = practice_s.laps.pick_driver(teammate)
    other_laps['LapsInStint'] = other_laps.groupby('Stint').cumcount() + 1

    # filtering out non-valid laps
    main_laps.pick_wo_box()
    main_laps = main_laps.loc[main_laps['TrackStatus'] == '1']
    main_laps.pick_quicklaps(1.07)

    other_laps.pick_wo_box()
    other_laps = other_laps.loc[other_laps['TrackStatus'] == '1']
    other_laps.pick_quicklaps(1.07)

    # lap time fuel correction
    main_laps['FuelCorrectedLapTime'] = main_laps['LapTime'].dt.total_seconds() + (0.035 * main_laps['LapsInStint'])
    other_laps['FuelCorrectedLapTime'] = other_laps['LapTime'].dt.total_seconds() + (0.035 * other_laps['LapsInStint'])

    Xm = main_laps[['TyreLife', 'Compound', 'TrackTemp']].copy()
    Xm['Compound'] = le.transform(Xm['Compound'])
    ym = main_laps['FuelCorrectedLapTime']

    Xt = other_laps[['TyreLife', 'Compound', 'TrackTemp']].copy()
    Xt['Compound'] = le.transform(Xt['Compound'])
    yt = other_laps['FuelCorrectedLapTime']

    # Train both models
    main_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xm,ym)

    other_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xt,yt)

    return {
        "models": {
            main_driver: main_model,
            teammate: other_model
        },
        "encoder": le,
        "baseline_track_temp": main_laps['TrackTemp'].mean(),
        "metadata": {
            "main_driver": main_driver,
            "teammate": teammate,
            "race_name": info[1],
            "year": info[0]
        }
    }
    


def prev_race_analysis(info, main_driver,teammate, le):
    race = fastf1.get_session(info[0],info[1],"R")
    race.load()

    # load times for each driver (no calculations needed for stint lengths though)
    main_laps = race.laps.pick_driver(main_driver)
    other_laps = race.laps.pick_driver(teammate)

    # filtering out non-valid laps
    main_laps.pick_wo_box()
    main_laps = main_laps.loc[main_laps['TrackStatus'] == '1']
    main_laps.pick_quicklaps(1.07)

    other_laps.pick_wo_box()
    other_laps = other_laps.loc[other_laps['TrackStatus'] == '1']
    other_laps.pick_quicklaps(1.07)

    # lap time fuel correction
    main_laps['FuelCorrectedLapTime'] = main_laps['LapTime'].dt.total_seconds() + (0.035 * main_laps['LapNumber'])
    other_laps['FuelCorrectedLapTime'] = other_laps['LapTime'].dt.total_seconds() + (0.035 * other_laps['LapNumber'])

    Xm = main_laps[['TyreLife', 'Compound', 'TrackTemp']].copy()
    Xm['Compound'] = le.transform(Xm['Compound'])
    ym = main_laps['FuelCorrectedLapTime']

    Xt = other_laps[['TyreLife', 'Compound', 'TrackTemp']].copy()
    Xt['Compound'] = le.transform(Xt['Compound'])
    yt = other_laps['FuelCorrectedLapTime']

    # Train both models
    main_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xm,ym)
    other_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xt,yt)

    return {
        "models": {
            main_driver: main_model,
            teammate: other_model
        },
        "encoder": le,
        "baseline_track_temp": main_laps['TrackTemp'].mean(),
        "metadata": {
            "main_driver": main_driver,
            "teammate": teammate,
            "race_name": info[1],
            "year": info[0]
        }
    }

def le_preperation():
    compounds = ['SOFT','MEDIUM','HARD','INTERMEDIATE','WET']
    le = LabelEncoder()
    le.fit(compounds)
    return le