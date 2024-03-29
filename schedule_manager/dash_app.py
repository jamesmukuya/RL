import pandas as pd
import numpy as np
#dash imports
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

#import plotly.graph_objects as go

rows=['a','b','c']
date_range = pd.date_range(start='2019-11-01',end='2019-11-30',freq='H')
date_list=date_range.tolist() #methods available incl. .time()
#df = pd.DataFrame(index=rows,columns=date_range)
	#for i in range date_range, if i%60==0: display the hours

VALID_USERNAME_PASSWORD_PAIRS = [('james','12345'),('susan','12345')]
# table page size


#########################
app = dash.Dash(__name__,assets_folder='static')
app.config['suppress_callback_exceptions'] = True
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(id='main-bg',className='flex flex-col min-w-12 sm:min-w-full bg-gray-200',children=[
	html.Button('open modal',id="myBtn"),
	html.Div(id='first-Modal',className='modal',children=[
		html.Div(className='modal-content')
	]),
	html.Div('print something',id='something'),
	html.Div(id='none',children=[],style={'display': 'none'}),
	html.Div(id='relative-parent',className='parent-grid rounded shadow-lg mx-1 bg-gray-500 mt-1 mb-2 border border-black h-full w-full',
	children=[
		html.Div(id='equip-nav',className='equip-nav bg-gray-300 px-1 mt-0 border border-black h-full'),
		html.Div(id='main-plot',className='main-plot can-scale bg-blue-500 mt-0 border border-black h-full overflow-scroll overflow-hidden')
	]),
	
])
"""
<link href="{{ url_for('static', filename='css/fontawesome/css/fontawesome.min.css') }}"
		rel="stylesheet" type="text/css">
{{url_for('static', filename='flights/new_flight.html')}}
------------------------------------------------------------------------------
for the form

"""




#print(df.index)
# plot the schedule from database on loading
@app.callback(Output('equip-nav','children'),
[Input('none','children')])
def insert_equip(tail):
	tails=['na','5a','5b','5c','5d','5e']
	tail=[]
	# looping over planned sched
	for reg in tails:
		if reg=="" or reg=='na':
			tail.append(html.Div(html.Button()))
		else:
			tail.append(html.Div(id='tail-'+ reg, children=[dcc.Checklist(id=reg,
			options=[
				{'label':reg,'value':reg}
			]),
			html.Button(html.I(className='fa fa-caret-right bg-black'),id=reg+'-tail-event',
				className='float-right',n_clicks=0)]))
	# adding using single event
	tail.append(html.Div(html.Button('5f')))
	#tail.append(html.I(className='fal fa-caret-right'))
	return tail

@app.callback(Output('main-plot','children'),
[Input('none','children')])
def insert_flight(flight):
	flight=[]
	time_btn_classes = 'timebtn'
	begin=1
	for date_hour in date_list:
		init_time = begin
		end_time = 30 + init_time
		flight.append(html.Button(str(date_hour),className=time_btn_classes,
					style={'grid-column-start':str(init_time),'grid-column-end':str(end_time),
							'grid-row-start':'1'}))
		begin = end_time
	# using single call events like button click
	# THE DEFAULT ITEMS FOR A FLIGHT ARE:
	flight.append(html.Div('div for stuff',className='flight',
		style={'grid-column-start':'7','grid-column-end':'65', 'grid-row-start':'3'},n_clicks=0))
	flight.append(html.Label('NBO',id='from-dep',className='label-from',
		style={'grid-column-start':'7','grid-column-end':'18', 'grid-row-start':'3'},n_clicks=0))
	flight.append(html.Label('MBA',id='to-dest',className='label-to',
		style={'grid-column-start':'54','grid-column-end':'65', 'grid-row-start':'3'},n_clicks=0))
	flight.append(html.Label('JAMES MUKUYA',id='cpt-',className='operating-capt',
		style={'grid-column-start':'19','grid-column-end':'53', 'grid-row-start':'3'},n_clicks=0))
	###################################################################################
	flight.append(html.Button('new flight',className='flight',
		style={'grid-column-start':'50','grid-column-end':'95', 'grid-row-start':'3'}))
	flight.append(html.Button('new flight',className='flight',
		style={'grid-column-start':'50','grid-column-end':'105', 'grid-row-start':'2'}))
	return flight

@app.callback(Output('something','children'),
			[Input('myBtn','n_clicks')])
def print_something(n_clicks):
	return f'button is clicked {n_clicks} times'












def main():
	app.run_server(debug=True)
	pass

if __name__ == '__main__':
    main()

