from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

def stint_analysis(data, le):
    # sort lap times based on stints
    data['LapsInStint'] = data.groupby('Stint').cumcount() + 1

    X = data[['TyreLife','Compound','TrackTemp']].copy()
    X['Compound'] = le.transform(X['Compound'])
    y = data[['FuelCorrectedLapTimes']].copy()

    model = RandomForestRegressor(n_estimators = 100, random_state=42).fit(X,y)

    return {
        "model": model,
        "encoder": le,
        "baseline_track_temp": data['TrackTemp'].mean(),
    }

def le_preparation():
    compounds = ['SOFT','MEDIUM','HARD','INTERMEDIATE','WET']
    le = LabelEncoder()
    le.fit(compounds)
    return le