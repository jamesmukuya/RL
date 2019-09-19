"""
Implement value iteration to obtain utility value of each state
"""
import gym
import numpy as np

# load the environment
env = gym.make('FrozenLake-v0')
s = env.reset() #to initialize the environment with 0 state
print(s)
print()

# value iteration
# initialize utilites of all states with zeros
U = np.zeros([env.observation_space.n])

# terminal states have utilities = their reward
U[15] = 1 # goal state
U[[5,7,11,12]] = -1 # hole states
termS = U[[5,7,11,12,15]] # terminal state

# set hyperparameters
y = 0.8 # discount factor
eps = 1e-3 # threshold of learning difference ie. prev_u - U

i = 0 # initialize count
while True:
	i+= 1
	prev_u = np.copy(U)
	for s in range(env.observation_space.n):
		q_sa = [sum([p *(r + y*prev_u[s_]) for p,s_,r,_ in env.env.P[s][a]]) for a in range(env.action_space.n)]
		# env.evn.P represents transition probabilities of the environment
		# p = probability, s_ = next state, r = reward, _ = done
		if s not in termS:
			U[s] = max(q_sa)

	if (np.sum(np.fabs(prev_u - U)) <= eps):
		print('Value iteration converged at {}' .format(i+1))
		break

print('After learning, printing utilities for each state')
print()
print(U[:4])
print(U[4:8])
print(U[8:12])
print(U[12:16])