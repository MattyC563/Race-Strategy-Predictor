from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

def stint_analysis(data, tyres_to_num):
    # sort lap times based on stints
    data['LapsInStint'] = data.groupby('Stint').cumcount() + 1

    X = data[['TyreLife','Compound','TrackTemp']].copy()
    X['Compound'] = X['Compound'].map(tyres_to_num)
    y = data['FuelCorrectedLapTimes'].copy()

    model = RandomForestRegressor(n_estimators = 100, random_state=42).fit(X,y)

    return {
        "model": model,
        "baseline_track_temp": data['TrackTemp'].mean(),
    }