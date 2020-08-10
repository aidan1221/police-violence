import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from states_dict import us_state_abbrev
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# population data from https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D
# police violence data from mappingpoliceviolence.org

race_df = pd.read_csv("race_data.csv")
police_violence_df = pd.read_excel("MPVDatasetDownload.xlsx")


data = police_violence_df.loc[:,["Victim's race", "State"]]

data.columns=["race", "state"]

states = sorted(list(set(data["state"])))

percent_killings_percent = []
total = 0
for s in states:

    percent_killings_percent.append((data.loc[((data.race == "Black") & (data.state == s)), "race"].count() / data.loc[(("unknown".lower() not in data.race) & (data.state == s)), "race"].count()) * 100)

police_killings_dict = {"state":states, "percent_police_killings_black":percent_killings_percent}

df = pd.DataFrame.from_dict(police_killings_dict)

state_abbrevs = [us_state_abbrev[s] for s in list(race_df.loc[:,"Location"])]

race_df["Location"] = race_df.replace(list(race_df["Location"]),state_abbrevs)

states = list(race_df.loc[:, "Location"])
populations = list(race_df.loc[:, "Black"] * 100)

assert len(states) == len(populations), print(f"{len(states)}, {len(populations)}")

race_pop_dict = {"state": states, "black_population": populations}

df2 = pd.DataFrame.from_dict(race_pop_dict)

df = df.join(df2.set_index('state'), on='state')
df["discrepancy"] = df["percent_police_killings_black"] - df["black_population"]



# https://plotly.com/python/choropleth-maps/#united-states-choropleth-map


fig = go.Figure(
    data=go.Choropleth(locations=df["state"],
                       z=df["discrepancy"],
                       locationmode="USA-states",
                       # colorscale=[[0,'moccasin'],[0.5, 'orangered'], [1, 'red']],
                       # colorscale=[[0,'lightcyan'], [1, 'midnightblue']],
                       colorscale=[[0, 'white'],[0.25,'moccasin'], [0.5, 'orangered'], [1, 'red']],
                       colorbar_title="% Discrepancy"))

fig.update_layout(
    title_text="Discrepancy between % Black people killed by police<br>and % Black population (2013-2020)",
    geo_scope="usa",
    height=900,
    width=1200)

fig.show()

fig = go.Figure(
    data=go.Choropleth(locations=df["state"],
                       z=df["black_population"],
                       locationmode="USA-states",
                       colorscale=[[0, 'white'],[0.25,'moccasin'], [0.5, 'orangered'], [1, 'red']],
                       colorbar_title="% Black population"
                       ))

fig.update_layout(
    title_text="% Black population (Census data 2018)",
    geo_scope="usa",
    height=900,
    width=1200)

fig.show()

