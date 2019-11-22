#dash imports
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import plotly.graph_objects as go

VALID_USERNAME_PASSWORD_PAIRS = [('james','12345'),('susan','12345')]
# table page size
page_size = 25

#########################
app = dash.Dash(__name__,assets_folder='static')

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
	html.Div(id='none',children=[],style={'display': 'none'}),
	html.Div(id='relative-parent',className='relative bg-gray-500',children=[
		html.Div('date 20rem',id='some-day',className='absolute border border-black border-r-1 border-b-0 border-l-0 pt-0 pb-0 h-screen z-50',
					style={'width':'96rem','margin-left':'0rem'}),
		#html.Button('Nexttt',className='absolute ml-2 mt-5 left-0 top-0 bg-gray-200 hover:bg-gray-400 text-gray-800 text-xs font-bold w-16 h-6 border-1 '),
		html.Div('date2 20rem',id='some-day2',className='absolute border border-black border-r-1 border-b-0 border-l-0 pt-0 pb-0 h-screen z-50',
					style={'width':'96rem','margin-left':'96rem'}),
	]),
	
	#html.Button('Prev',className='border-2 mx-2'),
	html.Div(id='btns',className='absolute flex inline-flex border-1 border-black mt-6',children=[
		html.Button('Prev',className='bg-blue-300 hover:bg-gray-400 text-gray-800 text-xs font-bold h-6 border border-black border-1 ',
						style={'width':'4rem'}),
		html.Button('Next',className='bg-gray-200 hover:bg-gray-400 text-gray-800 text-xs font-bold w-16 h-6 border border-black border-1 '),
		html.Button('Also Next',className='bg-gray-200 hover:bg-gray-400 text-gray-800 text-xs font-bold w-16 h-6 border border-black border-1 '),
		#html.Div(id='some-date',className='border border-black border-l-1 pt-0 pb-0'),
		html.Button('After div',className='bg-gray-200 hover:bg-gray-400 text-gray-800 text-xs font-bold w-16 h-6 border border-black border-1 '),
		html.Button('After div',className='bg-gray-200 hover:bg-gray-400 text-gray-800 text-xs font-bold w-16 h-6 border border-black border-1 '),
	]),
		html.Button('flight one',className='bg-green-400 hover:bg-gray-400 text-gray-800 text-xs font-bold h-8 border border-black border-1',
					style={'width':'8rem','margin-left':'16rem','margin-top':'12rem'})
])

"""
y=[1,1]
@app.callback(Output('sample-plot','figure'),
			[Input('none','children')])
def plot_bar(somebar):
	traces=[]
	layouts=[]
	charts = [go.Scatter(
					x=[1,2],
					y=y,
					fill='tonexty',
					fillcolor='darkviolet',
					#orientation='h',
					mode='lines',
					#stackgroup='one',
					marker={
						'line':{
							'width':1.0,
								}
							}
						),
				go.Scatter(
					x=[3,6],
					y=y,
					fill='tonexty',
					fillcolor = 'violet',
					#orientation='h',
					mode='lines',
					stackgroup='one',
					marker={
						'line':{
							'width':1.0,
								}
							}
						),
				go.Scatter(
					x=[5,38],
					y=y,
					mode='lines',
					line={
						'width':50
					},
					#stackgroup='z',
					marker={
						'line':{
							'width':1.0,
								}
							}
						),
				dcc.Checklist(id='chk-in-graph',options=[{
					'label':'gA', 'value':'fafa'
				}],
				value=['fafa'],)
		]
	for chart in charts:
		traces.append(chart)

	layout=go.Layout(
			#autosize=True,
			height=300,
			shapes=[
				go.layout.Shape(
					type='line',
					xref="x",yref="paper",
					x0=10,x1=10,y0=0,y1=1, layer='above',
					line_width=2
				)
			]
		)

	return {
		'data':traces,
		'layout':layout,
	}
"""
def main():
	app.run_server(debug=True)




if __name__ == '__main__':
    main()

