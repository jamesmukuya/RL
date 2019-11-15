#dash imports
import dash
import dash_table
import dash_auth


VALID_USERNAME_PASSWORD_PAIRS = [('james','12345'),('susan','12345')]
# table page size
page_size = 25

#########################
app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = dash_table.DataTable(
    id='schedule',
    columns=[{"name": i, "id": i,"selectable": True} for i in sched_df.columns],
    data=sched_df.to_dict('records'),
	fill_width=True,
	editable=True,
	sort_action='native',
	sort_mode="multi",
	column_selectable="single",
	row_selectable="multi",
    row_deletable=False,
    selected_columns=[],
    selected_rows=[],
	page_action="native",
    page_current= 0,
    page_size= page_size,
	fixed_rows={ 'headers': True, 'data': 0 },
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









if __name__ == '__main__':
    app.run_server(debug=True)