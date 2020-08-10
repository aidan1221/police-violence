import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from states_dict import us_state_abbrev
from sklearn.linear_model import LinearRegression

# population data from https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D
# police violence data from mappingpoliceviolence.org

race_df = pd.read_csv("race_data.csv")
police_violence_df = pd.read_excel("MPVDatasetDownload.xlsx", sheet_name="2013-2019 Killings by State")

killings_per_1000000 = police_violence_df.loc[:50,["State", "# Black people killed"]]
killings_per_1000000.loc[:,"# Black people killed"] = ((police_violence_df.loc[:50,"# Black people killed"] / police_violence_df.loc[:50,"African-American Alone"]) * 1000000)

killings_per_1000000.columns = ["State", "# Black people killed per 1000000 Black people"]

killings_per_1000000.loc[:,"Black_population"] = race_df.loc[:50,"Black"].copy() * 100


y = list(killings_per_1000000["# Black people killed per 1000000 Black people"])
x = list(killings_per_1000000["Black_population"])

# model = LinearRegression().fit(x, np.array(y).reshape(-1, 1))
#
# regression_vals = [(model.intercept_ + (model.coef_ * i)) for i in x]

killings_per_1000000 = killings_per_1000000.replace(np.nan, 0)

print(killings_per_1000000["# Black people killed per 1000000 Black people"])
# fig, ax = plt.subplots(nrows=1, ncols=1)
#
# ax.scatter(x, y, color='r')
# ax.plot(x, regression_vals, color='b')
#
# #
# fig.savefig("regression.png")

fig = px.scatter(x=x, y=y, trendline="ols")



fig2 = go.Figure(data=go.Scatter(x=killings_per_1000000["Black_population"],
                                y=killings_per_1000000["# Black people killed per 1000000 Black people"],
                                mode='markers',
                                marker=dict(size=(killings_per_1000000["# Black people killed per 1000000 Black people"] / 5)),
                                marker_color=killings_per_1000000["# Black people killed per 1000000 Black people"],
                                text=killings_per_1000000["State"], name="per capita by state vs population"))

fig2.add_trace(go.Scatter(fig.data[1], mode="lines", name="Least Squares Trendline"))

fig2.update_layout(
    title="Black people killed per million Black people in state <br>vs Percent Black population of a state",
    width=1000,
    height=500,
    xaxis_title="Percent Black population",
    yaxis_title="Police killings of Black people per million")

fig2.show()
