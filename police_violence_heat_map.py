import pandas as pd
import plotly.graph_objects as go
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
            pv_state_race_dict[s][race] = (num_pv_race["Victim's name"][s][race] / total) * 100

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

print(percent_violence_discrep)

df_dict = dict()

states = list(race_df["Location"])
codes = [us_state_abbrev[x] for x in states]
# df_dict["states"] = list(sorted(percent_violence_discrep.keys()))
df_dict["states"] = states
df_dict["codes"] = codes
df_dict["discrepancies"] = [x for x in [percent_violence_discrep[a] for a in codes]]

print(df_dict)

df_dict["states"].remove("District of Columbia")
df_dict["codes"].remove("DC")
df_dict["discrepancies"].remove(95.3833)


df = pd.DataFrame.from_dict(df_dict)

pop_df = race_df[["Location","Black"]].copy()
pop_df.columns = ["states", "population"]
print(pop_df)
pop_df = pop_df.drop(index=8).copy()
print(pop_df)
print(len(pop_df))
print(len(codes))
pop_df["codes"] = codes

print(pop_df)

# https://plotly.com/python/choropleth-maps/#united-states-choropleth-map


fig = go.Figure(
    data=go.Choropleth(locations=df["codes"],
                       z=df["discrepancies"],
                       locationmode="USA-states",
                       colorscale='Reds',
                       colorbar_title="% Discrepancy"))

fig.update_layout(
    title_text="Discrepancy between % Black people killed by police<br>and percent representation in population",
    geo_scope="usa")

fig.show()

fig = go.Figure(
    data=go.Choropleth(locations=pop_df["codes"],
                       z=pop_df["population"],
                       locationmode="USA-states",
                       colorscale='Reds',
                       colorbar_title="% population"))

fig.update_layout(
    title_text="Percent Black population",
    geo_scope="usa")

fig.show()
