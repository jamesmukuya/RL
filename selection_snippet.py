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
prev_cost2 = [18000,20000,50000,30000,65000,14000,10000,35000,40000,12000]
curr_cost = [3300,7000,2000,1000,2500,1500,6000,4000,1300,2000,1000]
next_cost = [x+y for x, y in zip(prev_cost,curr_cost)]
next_cost2 = np.add(prev_cost,curr_cost).tolist()

# the highest of prev_cost will be added to the lowest of curr_cost to get best cost
# 1. arrange the prev_cost in descending order and curr_cost in ascending then add

sorted_prev_cost = sorted(prev_cost,reverse=True)
sorted_curr_cost = sorted(curr_cost,reverse=False)
best_cost = np.add(sorted_prev_cost,sorted_curr_cost).tolist()
#print(best_cost)

# 2. items with an id i.e dataframe

asc_row_number = [] # row numbers for prev cost from highest to lowest
desc_row_number = [] # row numbers for curr cost from lowest to highest
df = pd.DataFrame(list(zip(id,prev_cost,curr_cost)),
				columns = ['id','prev_cost','curr_cost'])
#print(df)
next_tot_cost = df['prev_cost'].values + df['curr_cost'].values
df['next_tot_cost'] = next_tot_cost

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
		if r == j:
			# if value of the row is max, append its number in the container
			desc_row_number.append(row_numb_min)
			# remove the max number from the previous cost list
			curr_cost.remove(r)

#print(desc_row_number)
# get recommended cost column
recomm_cost = []
for r_num_min in desc_row_number:
	#print(r_num_min)
	curr_cost_row_val = df.iloc[r_num_min].curr_cost
	recomm_cost.append(curr_cost_row_val)
	#this val is inserted to the cell of df recomm cost as per index of asc_row_number
# add this column to the df

df['recomm_cost'] = recomm_cost
print(df)

"""
# get the values of the row numbers from the list
new_cost = []
for r_num_max,r_num_min in list(zip(asc_row_number,desc_row_number)):
	prev_cost_row_value = df.iloc[r_num_max].prev_cost
	curr_cost_row_value = df.iloc[r_num_min].curr_cost
	# add the Data Frame values of the lists given by row numbers
	new_cost.append(np.add(prev_cost_row_value,curr_cost_row_value))

# concatenate this new cost to the df
df['new_cost'] = new_cost
print(df)
"""
#print(new_cost)
#print(df.iloc[[3]].prev_cost) # gives a df obj
#print(df.iloc[3].prev_cost) # gives a series obj
