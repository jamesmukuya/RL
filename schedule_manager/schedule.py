"""
module to load a schedule and analyse the best cost.
gives suggestions on which equipments to swap or maintain.
considers the dep times to avoid selecting departed flights or flights too far ahead.
station recommended for change is base i.e NBO
"""

#load the imports
import os
import time
import numpy as np
import pandas as pd
from datetime import datetime

#dash imports
import dash
import dash_table
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

#plotly imports
import plotly.graph_objects as go
####################################################################################################
#SET PANDAS OPTIONS FOR DISPLAY
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.max_colwidth',500)
pd.set_option('display.width',None)

####################################################################################################
class Schedule:
	"""
	module for cleaning, munging and analyzing the loaded schedule
	"""
	pass
###################################################################################################
#LOAD THE EXCEL DOC
sched_loc = r'C:\Users\james\Documents\My Documents\Project Data\Sched'
sched_name = 'SIMPLIFIED.xlsx'
sched_path = os.path.join(sched_loc,sched_name)
sched_df = pd.read_excel(sched_path,sep=',')

#LOAD THE REQUIRED COLUMNS
sched_df = sched_df[['STD DATE','ST TIME','FLT NO', 'DEP', 'ARR', 'ACT J', 'ACT Y','TAIL', 'TYPE']]
sched_df.columns = [c.replace(' ','_') for c in sched_df.columns]

#DATA CLEANING
sched_df.fillna(np.nan)
sched_df.dropna(inplace=True)
#should reset the index after dropping na else the indices still reflect the earlier ones
sched_df.reset_index(inplace=True)

#PUT THE CORRECT TYPE COLUMNS AND WORK ON NA values
sched_df['STD_DATE'] = sched_df['STD_DATE'].astype(str)
sched_df['ST_TIME'] = sched_df['ST_TIME'].astype(int)
sched_df['ST_TIME'] = sched_df['ST_TIME'].astype(str)
sched_df['FLT_NO'] = sched_df['FLT_NO'].astype(int)
sched_df['FLT_NO'] = sched_df['FLT_NO'].astype(str)
sched_df['ACT_J'] = sched_df['ACT_J'].astype(int)
sched_df['ACT_Y'] = sched_df['ACT_Y'].astype(int)

flt_no = []
for k in sched_df['FLT_NO']:
	flt='a' + k
	flt_no.append(flt)
sched_df['FLT_NO'] = flt_no

SCHED_COLS = ['STD_DATE', 'ST_TIME','FLT_NO','DEP', 'ARR','ACT_J','ACT_Y','TAIL', 'TYPE']
schedule_df = sched_df[SCHED_COLS]

#RECTIFY SOME OF THE ST TIME CELLS WHICH CONTAIN ONLY 2 CHARACTERS
hr_min_cont = []
for tm in sched_df['ST_TIME']:
	if len(tm) < 3:
		zero_hour = '00'
		full_time = zero_hour + tm
		hr_min_cont.append(full_time)
		#print(full_time)
	elif len(tm) > 2:
		hr_min_cont.append(tm)

#NEW TIME
new_times = []
for stm2 in hr_min_cont:
	mins_only = stm2[-2:]
	hr_only = stm2[:-2]
	joined_time = hr_only +':'+ mins_only
	date_obj = datetime.strptime(joined_time,'%H:%M')
	time_obj = date_obj.time()
	new_times.append(time_obj)
	#print('time ',time_obj)

#NEW ST TIME COLUMN
sched_df['ST_TIME'] = new_times

#PLACE NEW COLUMN CONTAINING SCHED DEP DATETIME
sched_df['STD_DATETIME'] = sched_df['STD_DATE'].astype(str).map(str)+ ' '+ sched_df['ST_TIME'].astype(str)

#NEW COLS CONTAINING THE PREVIOUS TOTAL FLIGHT COST AND NEXT FLIGHT COST
prev_cost = np.random.uniform(low=40000.0,high=60000.0,size=len(sched_df['FLT_NO'].values)).tolist()
curr_cost = np.random.uniform(low=1000.0, high=20000.0,size=len(sched_df['FLT_NO'].values)).tolist()
sched_df['PREV_COST'] = prev_cost
sched_df['CURR_FLT_COST'] = curr_cost
sched_df['NEXT_FLT_COST'] = sched_df['PREV_COST'].to_numpy() + sched_df['CURR_FLT_COST'].to_numpy()

#SOLN PROPOSAL
asc_row_number = [] # row numbers for prev cost from highest to lowest
desc_row_number = [] # row numbers for curr cost from lowest to highest

sched_df['_prev_cost'] = prev_cost
sched_df['_curr_cost'] = curr_cost
# iterate over the dataframe
for _ in sched_df['PREV_COST'].values:	
	# iterate over the original previous cost list
	for j in prev_cost:
		# find the max value of the previous cost
		r = np.max(prev_cost)
		# get DataFrame row info. of the max value
		row_info_max = sched_df.loc[sched_df['PREV_COST'].values==r]
		# get DataFrame row number of the max value from row info
		row_numb_max = row_info_max.index.values.astype(int)[0]
		# set the cell data to Nan to prevent any dubplicated row numbers
		if row_numb_max in asc_row_number:
			#print(row_numb_max,'already present')
			sched_df.at[row_numb_max,'PREV_COST'] = np.nan

		if r == j:
			# if value of the row is max, append its number in the container
			asc_row_number.append(row_numb_max)
			# remove the max number from the previous cost list
			prev_cost.remove(r)

for _ in sched_df['CURR_FLT_COST'].values:	
	# iterate over the original previous cost list
	for j in curr_cost:
		# find the max value of the previous cost
		r = np.min(curr_cost)
		# get DataFrame row info. of the max value
		row_info_min = sched_df.loc[sched_df['CURR_FLT_COST'].values==r]
		# get DataFrame row number of the max value from row info
		row_numb_min = row_info_min.index.values.astype(int)[0]

		# set the cell data to Nan to prevent any dubplicated row numbers
		if row_numb_min in desc_row_number:
			#print(row_numb_max,'already present')
			sched_df.at[row_numb_min,'CURR_FLT_COST'] = np.nan
		if r == j:
			# if value of the row is min, append its number in the container
			desc_row_number.append(row_numb_min)
			# remove the max number from the previous cost list
			curr_cost.remove(r)
			
# PREPARED FLT NO
soln_flt_rte = []
soln_flt_num = []
for row_num in desc_row_number:
	try:
		new_dep_data = sched_df.iloc[row_num]['DEP']
		new_arr_data = sched_df.iloc[row_num]['ARR']
		new_flt_no = sched_df.iloc[row_num]['FLT_NO']
		new_rte = new_dep_data +'-'+ new_arr_data
		soln_flt_rte.append(new_rte)
		soln_flt_num.append(new_flt_no)
	except IndexError as e:
		# do something before production
		pass
#print(soln_flt_details[:5])
# create columns for recommended and suggested costs
sched_df['recomm_cost'] = np.nan
# for all row numbers in desc and asc row number, insert the value of the min to the row of max
x = list(zip(desc_row_number,asc_row_number))
#print(x[1][0])

for index in range(len(x)):
	try:
		recomm_val = sched_df.iloc[x[index][0]]._curr_cost
		sched_df.at[x[index][1],'recomm_cost'] = recomm_val
		
	except IndexError as IE:
		#print('<<ERROR at:>>', x[index][0],x[index][1],sched_df.iloc[x[index][1]])
		pass

# create col with the best value
sched_df['sugg_cost'] = sched_df['_prev_cost'].values + sched_df['recomm_cost'].values

#INITIAL FLT NO AND ROUTE
sched_df['RTE'] = sched_df['DEP']+'-'+sched_df['ARR']
sched_df['PROP_RTE'] = soln_flt_rte
sched_df['PROP_FLT_NO'] = soln_flt_num

#TOP FLIGHT COSTS
COST_COLS = ['STD_DATETIME', 'FLT_NO','ACT_J','ACT_Y', 'TAIL', 'PREV_COST','CURR_FLT_COST','RTE']
sched_df_nbo = sched_df.loc[sched_df['DEP'].to_numpy()=='NBO']
cost_df = sched_df_nbo[COST_COLS].sort_values('PREV_COST',ascending=False)

# SOLN PLAN DF
# check on dep times next
SOLN_COLS = ['FLT_NO','RTE','STD_DATETIME','PROP_FLT_NO', 'PROP_RTE','CURR_FLT_COST','recomm_cost']
soln_df = sched_df_nbo[SOLN_COLS]
soln_df = soln_df.loc[soln_df['PROP_RTE'].str.startswith('NBO')]

x_data = [i for i in pd.unique(sched_df_nbo['FLT_NO'].to_numpy())]
#print(soln_df[:20])

##################################################################################################################
	# SEPARATE HERE INTO ITS OWN FILE/MODULE
##################################################################################################################
VALID_USERNAME_PASSWORD_PAIRS = [('james','12345'),('susan','12345')]
# table page size
page_size = 25

##################################################################################################################

app = dash.Dash(__name__,assets_folder='static/css')

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.title = 'Schedule manager'
#flex-1 max-w-full sm:max-w-md md:max-w-lg lg:max-w-xl 
app.layout = html.Div([
	html.Div(className='flex lg:flex-row md:flex-col',
	children=[
		html.Div(id='full-sched-table',className='flex-auto rounded overflow-hidden shadow-lg px-4 py-2 mx-1 my-1',
		#style={'flex-direction':'column'},
		children=[
			html.Div('Schedule table', className='bg-red-500 text-blue font-bold rounded-t px-4 py-2'),
			dash_table.DataTable(
				id='schedule',
				columns=[{"name": i, "id": i,"selectable": True} for i in schedule_df.columns],
				data=schedule_df.to_dict(orient='records'),
				fill_width=True,editable=True, sort_action='native', sort_mode="multi", column_selectable="single",
				row_selectable="multi", row_deletable=False, selected_columns=[], selected_rows=[], page_action="native",
				page_size = page_size, page_current= 0, fixed_rows={ 'headers': True, 'data': 0 }, 
				style_header={
					'fontWeight': 'bold',
					'fill_width':False,
				},
				style_cell={
					'height':'auto',
					'minWidth': '0px', 'width': '50px', 'maxWidth': '180px',
					'overflow': 'hidden',
					'textOverflow': 'ellipsis',
					'textAlign':'left',
					#'whiteSpace':'normal',
				},
				style_table={
					'overflowX':'scroll',
					'maxHeight':'600px',
				},
				style_data_conditional=[
					{
						'if': {'row_index': 'odd'},
						'backgroundColor': 'rgb(248, 248, 248)'
					},
					{
						'if': {
							'column_id': 'DEP',
							'filter_query': '{DEP} eq NBO'
						},
						'backgroundColor': '#3D9970',
						'color': 'white',
					},
				],
			)	
				]),
		html.Div(id='top-cost-table',className='flex-auto rounded overflow-hidden shadow-lg px-4 py-2 mx-1 my-1',
			#style={'flex-direction':'column'},
			children=[
			html.Div('Top 20 costs ex NBO', className='bg-red-500 text-blue font-bold rounded-t px-4 py-2'),
			dash_table.DataTable(
				id='flt-costs',
				columns=[{"name": i, "id": i,"selectable": True} for i in cost_df.columns],
				data=cost_df[:20].to_dict('records'),
				fill_width=True,editable=False, sort_action='native', sort_mode="multi", column_selectable="single",
				row_selectable=False, row_deletable=False, selected_columns=[], selected_rows=[], page_action="native",
				page_size = page_size, page_current= 0, fixed_rows={ 'headers': True, 'data': 0 }, 
				style_header={
					'fontWeight': 'bold',
					'backgroundColor': '#4299e1'
				},
				style_cell={
					'minWidth': '0px', 'width': '50px', 'maxWidth': '180px',
					'overflow': 'hidden',
					'textOverflow': 'ellipsis',
					'textAlign':'left',
					#'whiteSpace':'normal',
				},
				style_table={
					'overflowX':'scroll',
					'maxHeight':'600px',
				},
				style_data_conditional=[
					{
						'if': {'row_index': 'odd'},
						'backgroundColor': 'rgb(248, 248, 248)'
					}
					],
				
			)	
				]),
		# new div here
		]),
	# new div here
	html.Div(className='flex lg:flex-row md:flex-col', children=[
		html.Div(id='soln-plan-div',className='flex-auto rounded overflow-hidden shadow-lg px-4 py-2 mx-1 my-1',
			#style={'flex-direction':'column'},
			children=[
			html.Div('Solution Plan: Pre-plan', className='bg-red-500 text-blue font-bold rounded-t px-4 py-2'),
			dash_table.DataTable(
				id='soln-plan-table',
				columns=[{"name": i, "id": i,"selectable": True} for i in soln_df.columns],
				data=soln_df.to_dict('records'),
				fill_width=False,editable=False, sort_action='native', sort_mode="multi", column_selectable="single",
				row_selectable=False, row_deletable=False, selected_columns=[], selected_rows=[], page_action="native",
				page_size = page_size, page_current= 0, fixed_rows={ 'headers': True, 'data': 0 }, 
				css=[{'selector':'.previous-page','rule':'background-color:#e2e8f0;border-radius: .25rem;'},
					{'selector':'.next-page','rule':'background-color:#90cdf4; margin: 0.5rem; border-radius: .25rem;'},
					],
				style_header={
					'fontWeight': 'bold',
					'backgroundColor': '#4299e1',
					'whiteSpace':'normal',
					#'width':'7%'
				},
				style_cell={
					'minWidth': '0px','maxWidth': '180px',
					'overflow': 'hidden',
					#'textOverflow': 'ellipsis',
					'textAlign':'left',
					'whiteSpace':'normal',
					#'height':'auto'
				},
				style_table={
					'overflowX':'scroll', 'overflowY':'scroll',
					'maxHeight':'600px',
				},
				style_data_conditional=[
					{
						'if': {'row_index': 'odd'},
						'backgroundColor': 'rgb(248, 248, 248)'
					}
					],
				
			)	
				]),
		html.Div(id='cost-graph-div',className='flex-auto rounded overflow-hidden shadow-lg px-4 py-2 mx-1 my-1',
		children=[
			html.Div('Current vs Recommended cost',className='text-blue font-bold rounded-t px-4 py-2'),
			html.Div([
				dcc.Graph(id='cost-graph',
				figure={
					'data':[go.Scatter(
							x = x_data,
							y = [j for j in soln_df['CURR_FLT_COST'].to_numpy()],
							mode='lines',
							name='current cost'
						),
							go.Scatter(
							x=x_data,
							y=[j for j in soln_df['recomm_cost'].to_numpy()],
							mode='lines',
							name='recommended cost'
							)],
					'layout':go.Layout(
						autosize=False,
						width=800,
						height=600,
						legend={
							'orientation':'h',
							'yanchor':'top'
						},
						margin={
							'r':2
						},
						paper_bgcolor='#ebf8ff',
						plot_bgcolor='#ebf8ff'
					)
				})
			]),
			html.Hr(),
			html.Div(id='none',children=[],style={'display': 'none'}),
    		html.Div(id='my-div')
		])
	])
		
])	

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='none', component_property='children')]
)
def update_output_div(something):
	# you can put anything in the fxn. no need of providing pos arg to it
	# for now we place a hidden empty div without any children in order to have it in the callback
	input_value='nothing'

	return 'You\'ve entered "{}"'.format(input_value)

"""
callback not working
@app.callback(Output('cost-graph','figure'))
def draw_graph():

	traces = []
	x = [i for i in pd.unique(sched_df_nbo['FLT_NO'].to_numpy())]
	charts = [go.Scatter(
							x = x,
							y = [j for j in soln_df['CURR_FLT_COST'].to_numpy()],
							mode='lines',
							name='current cost'
						),
				go.Scatter(
							x=x,
							y=[j for j in soln_df['recomm_cost'].to_numpy()],
							mode='lines',
							name='recommended cost'
							)
			]
	for chart in charts:
		traces.append(chart)
		print(traces)

	return {
		'data': [chart for chart in charts],
		'layout':go.Layout(
					autosize=False,
					width=800,
					height=600,
					legend={
						'orientation':'h',
						'yanchor':'top'
					},
					margin={
						'r':2
					},
					paper_bgcolor='#ebf8ff',
					plot_bgcolor='#ebf8ff'
				)
			}
"""


def main():
	app.run_server(debug=True)





if __name__ == '__main__':
    main()
	
