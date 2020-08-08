import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import iplot
import states_dict

police_killings_df = pd.read_csv('PoliceKillings.csv')
killings_by_state_df = pd.read_csv('KillingsByState.csv')
individual_victims_df = pd.read_csv('IndividualVictims.csv')

black_population = killings_by_state_df.AfricanAmericanAlone
black_ppl_killed = killings_by_state_df.BlackPeopleKilled
black_killed_per_population = []

white_population = killings_by_state_df.WhiteAmericanAlone
white_ppl_killed = killings_by_state_df.WhitePeopleKilled
white_killed_per_population = []

ratio_black_to_white_killed = []

for i,j in zip(black_population, black_ppl_killed):
    black_killed_per_population.append(j/i*1000000)
for i,j in zip(white_population, white_ppl_killed):
    white_killed_per_population.append(j/i*1000000)
for i,j in zip(black_killed_per_population, white_killed_per_population):
    ratio_black_to_white_killed.append(i/j)

highest_disparity_states = ['AK', 'MA', 'NE', 'NJ', 'IL', 'UT', 'DC', 'RI']



#Police killings over time
opt = []
opts = []
for i in range(0, len(highest_disparity_states)):
    opt = dict(
        target = individual_victims_df['State'][[i]].unique(), value = dict(marker = dict(color = highest_disparity_states[i]))
    )
    opts.append(opt)

data = [dict(name = 'Alaska', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
			    transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'AK')]),
		dict(name = 'Massachusetts', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'MA')]),
		dict(name = 'Nebraska', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'NE')]),
		dict(name = 'New Jersey', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'NJ')]),
		dict(name = 'Illinois', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'IL')]),
		dict(name = 'Utah', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'UT')]),
		dict(name = 'District of Columbia', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'DC')]),
		dict(name = 'Rhode Island', type = 'line', x = individual_victims_df.DateOfIncident, y = individual_victims_df.Count, mode = 'lines', text = individual_victims_df.State, hoverinfo = 'y+text',
				transforms = [dict(type = 'filter', target = individual_victims_df['State'], operation = '=', value = 'RI')])				
]

layout = dict(title = 'Killings over time')
fig_dict = dict(data=data, layout=layout)
pio.show(fig_dict, validate=False)



#Number of black victims vs white victims per state
kbs_x=killings_by_state_df.State
kbs_y=black_killed_per_population
kbs_x_sorted = [kbs_x for _, kbs_x in sorted(zip(kbs_y,kbs_x))]
kbs_y_sorted = sorted(kbs_y)

kbs_fig = go.Figure(data=[
    go.Bar(name='Black people killed', x=kbs_x_sorted, y=kbs_y_sorted),
    go.Bar(name='White people killed', x=killings_by_state_df.State, y=white_killed_per_population)
])
kbs_fig.update_layout(barmode='group')
kbs_fig.show()



#Ratio of black victims to white victims
kbs_ratio_x=killings_by_state_df.State
kbs_ratio_y=ratio_black_to_white_killed
kbs_ratio_x_sorted = [kbs_ratio_x for _, kbs_ratio_x in sorted(zip(kbs_ratio_y,kbs_ratio_x))]
kbs_ratio_y_sorted = sorted(kbs_ratio_y)

kbs_ratio_fig = go.Figure(data=[
    go.Bar(name='Ratio of Black victims to White victims', x=kbs_ratio_x_sorted, y=kbs_ratio_y_sorted)
])
kbs_ratio_fig.update_layout(barmode='group')
kbs_ratio_fig.show()
