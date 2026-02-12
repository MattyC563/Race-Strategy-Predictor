import pandas as pd

def race_strategy_creator(race_model, le, total_laps, delta, avg_temp):
    results = []

    # Testing 1-Stop: Medium -> Hard
    for pit_lap in range(15, 40):
        # Stint 1: Mediums
        s1_time = 0
        for age in range(1, pit_lap + 1):
            p = race_model.predict([[age, le.transform(['MEDIUM'])[0], avg_temp]])[0]
            s1_time += (p + delta) - (0.035 * age) # Apply pace delta and fuel burn
            
        # Pit Stop Loss
        pit_loss = 23.0 
        
        # Stint 2: Hards
        s2_time = 0
        for age in range(1, (total_laps - pit_lap) + 1):
            p = race_model.predict([[age, le.transform(['HARD'])[0], avg_temp]])[0]
            # Cumulative lap is (pit_lap + age)
            s2_time += (p + delta) - (0.035 * (pit_lap + age))
            
        total_time = s1_time + pit_loss + s2_time
        results.append({'pit_lap': pit_lap, 'total_time': total_time})
        
    return pd.DataFrame(results).sort_values('total_time').iloc[0]