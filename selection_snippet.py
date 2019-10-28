"""
Created 18/10/2019 by James M. Okinda
This snippet is made to check the best swap alternative.
It considers the previous, current and next cost = (previous cost + current cost).
The code attempts to reduce the next cost by swapping current cost hence producing
a new best cost.
Assumptions made are all other costs are the same i.e no hidden costs
"""
import numpy as np
import pandas as pd

id = [1,2,3,4,5,6,7,8,9,10,11]
prev_cost = [18000,20000,50000,30000,65000,14000,10000,30000,35000,40000,12000]
curr_cost = [3300,7000,2000,1000,2500,1500,6000,4000,1300,2000,1000]
#next_cost = [x+y for x, y in zip(prev_cost,curr_cost)]
next_cost = np.add(prev_cost,curr_cost).tolist()

# the highest of prev_cost will be added to the lowest of curr_cost to get best cost
# 1. arrange the prev_cost in descending order and curr_cost in ascending then add

sorted_prev_cost = sorted(prev_cost,reverse=True)
sorted_curr_cost = sorted(curr_cost,reverse=False)
best_cost = np.add(sorted_prev_cost,sorted_curr_cost).tolist()
#print(best_cost)

# 2. items with an id e.g dataframe or database

asc_row_number = [] # row numbers for prev cost from highest to lowest
desc_row_number = [] # row numbers for curr cost from lowest to highest
df = pd.DataFrame(list(zip(id,prev_cost,curr_cost)),
				columns = ['id','prev_cost','curr_cost'],dtype=float)
#df2 = df.copy()
next_tot_cost = df['prev_cost'].values + df['curr_cost'].values
df['next_tot_cost'] = next_tot_cost
df['_prev_cost'] = prev_cost
df['_curr_cost'] = curr_cost
# iterate over the dataframe
for _ in df['prev_cost'].values:	
	# iterate over the original previous cost list
	for j in prev_cost:
		# find the max value of the previous cost
		r = np.max(prev_cost)
		# get DataFrame row info. of the max value
		row_info_max = df.loc[df['prev_cost'].values==r]
		# get DataFrame row number of the max value from row info
		row_numb_max = row_info_max.index.values.astype(int)[0]

		# set the cell data to Nan to prevent any dubplicated row numbers
		if row_numb_max in asc_row_number:
			#print(row_numb_max,'already present')
			df.at[row_numb_max,'prev_cost'] = np.nan

		if r == j:
			# if value of the row is max, append its number in the container
			asc_row_number.append(row_numb_max)
			# remove the max number from the previous cost list
			prev_cost.remove(r)

for _ in df['curr_cost'].values:	
	# iterate over the original previous cost list
	for j in curr_cost:
		# find the max value of the previous cost
		r = np.min(curr_cost)
		# get DataFrame row info. of the max value
		row_info_min = df.loc[df['curr_cost'].values==r]
		# get DataFrame row number of the max value from row info
		row_numb_min = row_info_min.index.values.astype(int)[0]

		# set the cell data to Nan to prevent any dubplicated row numbers
		if row_numb_min in desc_row_number:
			#print(row_numb_max,'already present')
			df.at[row_numb_min,'curr_cost'] = np.nan
		if r == j:
			# if value of the row is max, append its number in the container
			desc_row_number.append(row_numb_min)
			# remove the max number from the previous cost list
			curr_cost.remove(r)

# create an empty column
df['recomm_cost'] = np.nan
# for all row numbers in desc and asc row number, insert the value of the min to the row of max
#df.at[4,'recomm_cost'] = 25000
x = list(zip(desc_row_number,asc_row_number))
#print(x[1][0])
i=0
for _ in range(len(x)):
	recomm_val = df.iloc[x[i][0]]._curr_cost
	df.at[x[i][1],'recomm_cost'] = recomm_val
	i+=1
# create col with the best value
df['sugg_cost'] = df['_prev_cost'].values + df['recomm_cost'].values
#print(df)

