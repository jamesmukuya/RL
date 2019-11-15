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

#PUT THE CORRECT TYPE COLUMNS AND WORK ON NA values
sched_df['STD_DATE'] = sched_df['STD_DATE'].astype(str)
sched_df['ST_TIME'] = sched_df['ST_TIME'].astype(int)
sched_df['ST_TIME'] = sched_df['ST_TIME'].astype(str)
sched_df['FLT_NO'] = sched_df['FLT_NO'].astype(int)
sched_df['ACT_J'] = sched_df['ACT_J'].astype(int)
sched_df['ACT_Y'] = sched_df['ACT_Y'].astype(int)

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
prev_cost = np.random.randint(low=40000,high=60000,size=len(sched_df['FLT_NO'].values))
curr_cost = np.random.randint(low=1000, high=20000,size=len(sched_df['FLT_NO'].values))
sched_df['PREV_COST'] = prev_cost
sched_df['CURR_FLT_COST'] = curr_cost
sched_df['NEXT_FLT_COST'] = sched_df['PREV_COST'].values + sched_df['CURR_FLT_COST'].values
#sched_df = sched_df.columns.str.replace(' ','_')
#TOP 20 FLIGHT COSTS
COLS = ['STD_DATETIME', 'FLT_NO','ACT_J','ACT_Y', 'TAIL', 'PREV_COST','CURR_FLT_COST']
cost_df = sched_df[COLS].sort_values('PREV_COST',ascending=False)

#print(cost_df.head())

#print(len(prev_cost))
##################################################################################################################
	# SEPARATE HERE INTO ITS OWN FILE/MODULE
##################################################################################################################
VALID_USERNAME_PASSWORD_PAIRS = [('james','12345'),('susan','12345')]
# table page size
page_size = 25

#########################

app = dash.Dash(__name__,assets_folder='static/css')

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.title = 'my app'
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
				columns=[{"name": i, "id": i,"selectable": True} for i in sched_df.columns],
				data=sched_df.to_dict('records'),
				fill_width=True,editable=True, sort_action='native', sort_mode="multi", column_selectable="single",
				row_selectable="multi", row_deletable=False, selected_columns=[], selected_rows=[], page_action="native",
				page_size = page_size, page_current= 0, fixed_rows={ 'headers': True, 'data': 0 }, 
				style_header={
					'fontWeight': 'bold'
				},
				style_cell={
					'minWidth': '0px', 'width': '50px', 'maxWidth': '180px',
					'overflow': 'hidden',
					'textOverflow': 'ellipsis',
					'textAlign':'left'
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
				style_cell_conditional=[
					{'if': {'column_id': 'FLT NO'},
					'width': '5%'},
					{'if': {'column_id': 'DEP'},
					'width': '5%'},
					{'if':{'column_id':'ARR'},
					'width':'5%'},
					{'if':{'column_id':'ACT J'},
					'width':'5%'},
					{'if':{'column_id':'ACT Y'},
					'width':'5%'},
					{'if':{'column_id':'TAIL'},
					'width':'5%'},
					{'if':{'column_id':'TYPE'},
					'width':'5%'},
				]
			)	
				]),
		html.Div(id='top-cost-table',className='flex-auto rounded overflow-hidden shadow-lg px-4 py-2 mx-1 my-1',
			#style={'flex-direction':'column'},
			children=[
			html.Div('Top 20 flight costs', className='bg-red-500 text-blue font-bold rounded-t px-4 py-2'),
			dash_table.DataTable(
				id='flt-costs',
				columns=[{"name": i, "id": i,"selectable": True} for i in cost_df.columns],
				data=cost_df[:20].to_dict('records'),
				fill_width=True,editable=False, sort_action='native', sort_mode="multi", column_selectable="single",
				row_selectable="multi", row_deletable=False, selected_columns=[], selected_rows=[], page_action="native",
				page_size = page_size, page_current= 0, fixed_rows={ 'headers': True, 'data': 0 }, 
				style_header={
					'fontWeight': 'bold',
					'backgroundColor': '#4299e1'
				},
				style_cell={
					'minWidth': '0px', 'width': '50px', 'maxWidth': '180px',
					'overflow': 'hidden',
					'textOverflow': 'ellipsis',
					'textAlign':'left'
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
				])
		])
	
	])	










if __name__ == '__main__':
    app.run_server(debug=True)
