import pandas as pd

def race_strategy_creator(model, num_to_tyre, total_laps, avg_temp, pit_loss_time, track_evo, event_probabilities, poss_strategies, fuel_burn, pace_delta=0):
    def calculate_lap_time(abs_lap, tyre_age, comp_num):
        base_time = predicted_base_paces[comp_num][tyre_age]
        fuel_effect = fuel_burn * abs_lap
        evo_effect = track_evo * abs_lap
        final_time = base_time + pace_delta - fuel_effect - evo_effect
        return final_time
    
    simulation_results = []
    predicted_base_paces = {0: {}, 1: {}, 2: {}}

    for comp in [0,1,2]:
        for age in range(1, total_laps + 1):
            pred_df = pd.DataFrame([[age, comp, avg_temp]], columns=['TyreLife','Compound','TrackTemp'])
            predicted_base_paces[comp][age] = model['model'].predict([[age, comp, avg_temp]])[0]

    for strat in poss_strategies:
        strat_len = len(strat)
        strat_names = [num_to_tyre[comp] for comp in strat]
        strat_label = " -> ". join(strat_names)

        # 1 stop strategies
        if strat_len == 2:
            c1, c2 = strat[0], strat[1]

            for pit_lap in range(5, total_laps - 5):
                total_race_time = 0
                abs_lap = 1

                # Stint 1
                for age in range(1, pit_lap + 1):
                    total_race_time += calculate_lap_time(abs_lap, age, c1)
                    abs_lap += 1

                total_race_time += pit_loss_time

                # Stint 2
                stint_2_laps = total_laps - pit_lap
                for age in range(1, stint_2_laps + 1):
                    total_race_time += calculate_lap_time(abs_lap, age, c2)
                    abs_lap += 1

                simulation_results.append({
                    'Strategy Name': f"1-Stop ({strat_label})",
                    'Pit 1 Lap': pit_lap,
                    'Pit 2 Lap': None,
                    'Total Time': total_race_time
                })

        elif strat_len == 3:
            c1, c2, c3 = strat[0], strat[1], strat[2]

            for pit_1_lap in range(4, total_laps - 24):
                for pit_2_lap in range(pit_1_lap + 10, total_laps - 9):
                    total_race_time = 0
                    abs_lap = 1

                    # Stint 1
                    for age in range(1, pit_1_lap + 1):
                        total_race_time += calculate_lap_time(abs_lap, age, c1)
                        abs_lap += 1

                    total_race_time += pit_loss_time

                    # Stint 2
                    stint_2_laps = pit_2_lap - pit_1_lap
                    for age in range(1, stint_2_laps + 1):
                        total_race_time += calculate_lap_time(abs_lap, age, c2)
                        abs_lap += 1

                    total_race_time += pit_loss_time

                    # Stint 3
                    stint_3_laps = total_laps - pit_2_lap
                    for age in range(1, stint_3_laps + 1):
                        total_race_time += calculate_lap_time(abs_lap, age, c3)
                        abs_lap += 1

                    simulation_results.append({
                        "Strategy Name": f"2-Stop ({strat_label})",
                        "Pit 1 Lap": pit_1_lap,
                        "Pit 2 Lap": pit_2_lap,
                        "Total Time": total_race_time
                    })

    df_sim_results = pd.DataFrame(simulation_results)
    best_strategy = df_sim_results.sort_values(by="Total Time")

    return best_strategy
    