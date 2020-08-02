import pandas as pd
import numpy as np
from states_dict import us_state_abbrev

race_df = pd.read_csv("race_data.csv")
police_violence_df = pd.read_excel("MPVDatasetDownload.xlsx")

pv_state_race_dict = dict()
state_race_dict = dict()


states_mpv = list(set(police_violence_df["State"]))
races_mpv = list(set(police_violence_df["Victim's race"]))
states_mpv.sort()

num_pv_race = police_violence_df.groupby(["State", "Victim's race"]).count()

for s in states_mpv:
    total = 0
    races = list(num_pv_race["Victim's name"][s].index)
    for race in races:
        if "unknown" not in race.lower():
            total += num_pv_race["Victim's name"][s][race]
    for race in races:
        if "unknown" not in race.lower():
            if s not in pv_state_race_dict:
                pv_state_race_dict[s] = dict()
            if race not in pv_state_race_dict[s]:
                pv_state_race_dict[s][race] = dict()
            pv_state_race_dict[s][race] = num_pv_race["Victim's name"][s][race] / total

print(pv_state_race_dict)

for _, row in race_df.iterrows():
    if row["Location"] not in state_race_dict:
        state = us_state_abbrev[row["Location"]]
        state_race_dict[state] = dict()
    for col in race_df.columns:
        if col != "Two Or More Races" and col != "Total" and col != "Location":
            if col not in state_race_dict[state]:
                state_race_dict[state][col] = dict()

            state_race_dict[state][col] = row[col]

percent_violence_discrep = dict()

for state in state_race_dict.keys():
    print(state + ":")
    print(f"\tBlack population: {state_race_dict[state]['Black']}")
    try:
        print(f"\tPercent Affected by police violence: {pv_state_race_dict[state]['Black']}")
        print(
            f"\t\tDIFFERENCE: {float(pv_state_race_dict[state]['Black']) - float(state_race_dict[state]['Black']):.4f}")
        percent_violence_discrep[state] = round(float(pv_state_race_dict[state]['Black']) - float(
            state_race_dict[state]['Black']), 4)
    except KeyError as e:
        print("\t**No police violence data from this state or none recorded for Black individuals**")
        percent_violence_discrep[state] = 0


sorted_by_largest_discrep = sorted(percent_violence_discrep.items(), key=lambda x: x[1], reverse=True)

print(sorted_by_largest_discrep)

