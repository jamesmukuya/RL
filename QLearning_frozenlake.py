"""
implementing a basic Q-Learning algorithm to make an agent learn how to
navigate across frozen lake of 16 grids, from the start to the goal without
falling into the hole
"""

#import the dependencies
import gym
import numpy as np

#load the environment

env = gym.make('FrozenLake-v0')
s = env.reset()
print("initial state",s)

#display the environment
env.render()

#type and number of actions
print(env.action_space)

#type and number of states
print(env.observation_space)

print('Number of actions:',env.action_space.n)
print('Number of observations:',env.observation_space.n)
print()

#Epsilon-greedy approach for Exploration and Exploitation of state-action space
def epsilon_greedy(Q,s,na):
	"""
	Q = Q-Value parameter
	s = state parameter
	na = action parameter
	"""
	epsilon = 0.3
	p = np.random.uniform(low=0,high=1)
	if p > epsilon:
		return np.argmax(Q[s,:])
	else:
		return env.action_space.sample()

#initialize Q table with zeros
Q = np.zeros([env.observation_space.n, env.action_space.n])

#set hyperparameters
lr = 0.5 #learning rate
y = 0.9 #discount factor
eps = 100000 #total episodes

for i in range(eps):
	s = env.reset()
	t = False
	while (True):
		a = epsilon_greedy(Q, s, env.action_space.n)
		s_,r,t,_ = env.step(a)
		#s_ = new state, r=reward at state, t=terminal, _ = end(True/False)
		if (r==0):
			if t==True:
				r = -5 #we have landed in a hole and game ends
				Q[s_] = np.ones(env.action_space.n) *r #in terminal state Q, value = reward
			else:
				r = -1 #give negative rewards to prevent long routes

		if (r==1):
			r = 100 #a good reward for the right state and action
			Q[s_] = np.ones(env.action_space.n) *r #in terminal state Q, value = reward

		#updating of a Q value for a state-action pair i.e Q(s,a)
		Q[s,a] = Q[s,a] + lr *(r + y *np.max(Q[s_,a]) - Q[s,a])
		s = s_
		if (t==True):
			break

print('Q-table')
print(Q)
print()

print('Output after learning')
print()

s = env.reset()
env.render()
while (True):
	a = np.argmax(Q[s])
	s_,r,t,_ = env.step(a)
	print('+=' *10)
	env.render()
	s = s_
	if (t==True):
		break
