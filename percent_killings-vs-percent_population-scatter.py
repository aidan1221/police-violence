import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from states_dict import us_state_abbrev
from sklearn.linear_model import LinearRegression


def get_scatter_percentages(df):
    fig1 = px.scatter(df, x="black_population", y="percent_police_killings_black", trendline="ols")

    fig2 = go.Figure(data=go.Scatter(x=df["black_population"],
                                     y=df["percent_police_killings_black"],
                                     mode="markers",
                                     marker=dict(
                                         size=(10 + (df["percent_police_killings_black"]/2))),
                                     marker_color=df["percent_police_killings_black"],
                                     text=df["state"],
                                     name="percent police killings Black vs percent Black population"))

    print(fig1.data[1])

    fig2.add_trace(go.Scatter(x=fig1.data[1].x, y=fig1.data[1].y, mode="lines", name="Least Squares Trendline",
                              marker_color="blue"))
    fig2.add_trace(go.Scatter(x=df["black_population"], y=df["black_population"], mode="lines", marker_color="red",
                              name="1:1 population correlation"))

    fig2.update_layout(
        title="% police killings that were Black people <br>vs % Black population of state",
        width=1000,
        height=500,
        xaxis_title="% Black population",
        yaxis_title="% Police Killings Black")

    fig2.show()


def get_scatter_discrepancy(df):
    fig1 = px.scatter(df, x="black_population", y="discrepancy", trendline="ols")

    fig2 = go.Figure(data=go.Scatter(x=df["black_population"],
                                     y=df["discrepancy"],
                                     mode="markers",
                                     marker=dict(size=(10 + (0.5 * df["discrepancy"]))),
                                     marker_color=df["discrepancy"],
                                     text=df["state"],
                                     name="Discrepancy between percent police killingsBlack "
                                          "<br>vs percent Black population"))

    print(fig1.data[1])

    fig2.add_trace(go.Scatter(x=fig1.data[1].x, y=fig1.data[1].y, mode="lines", name="Least Squares Trendline",
                              marker_color="blue"))

    fig2.update_layout(
        title="Discrepancy between % police killings that were Black people<br>vs % Black population of state",
        width=1000,
        height=500,
        xaxis_title="% Black population",
        yaxis_title="Discrepancy % Police Killings Black vs % Black Population")

    fig2.show()


race_df = pd.read_csv("race_data.csv")
police_violence_df = pd.read_excel("MPVDatasetDownload.xlsx")


data = police_violence_df.loc[:, ["Victim's race", "State"]]

data.columns = ["race", "state"]

states = sorted(list(set(data["state"])))

percent_killings_percent = []
for s in states:

    percent_killings_percent.append(
        (data.loc[((data.race == "Black") & (data.state == s)), "race"].count()
         / data.loc[(("unknown".lower() not in data.race) & (data.state == s)), "race"].count()) * 100)

police_killings_dict = {"state": states, "percent_police_killings_black": percent_killings_percent}

df = pd.DataFrame.from_dict(police_killings_dict)

state_abbrevs = [us_state_abbrev[s] for s in list(race_df.loc[:, "Location"])]

race_df["Location"] = race_df.replace(list(race_df["Location"]), state_abbrevs)

states = list(race_df.loc[:, "Location"])
populations = list(race_df.loc[:, "Black"] * 100)

assert len(states) == len(populations), print(f"{len(states)}, {len(populations)}")

race_pop_dict = {"state": states, "black_population": populations}

df2 = pd.DataFrame.from_dict(race_pop_dict)

df = df.join(df2.set_index('state'), on='state')

df["discrepancy"] = df["percent_police_killings_black"] - df["black_population"]


get_scatter_discrepancy(df)

get_scatter_percentages(df)
