import numpy as np
import matplotlib.pyplot as plt 

class GridWorld(object):
	"""
	Create a m * n grid.
	Our agent should be able to find the EXIT which is at the bottom right corner of the grid
	*state space is all states minus the terminal state
	*state space plus is all states including the terminal state
	*action space is a dict mapping of Up, Down, Left, Right across the grid
	"""
	def __init__(self, m, n, *args, **kwargs):
		self.grid = np.zeros((m,n)) # set states to zeros
		self.m = m # rows
		self.n = n # columns
		self.stateSpace = [i for i in range(self.m*self.n)] # state minus terminal
		self.stateSpace.remove(self.m*self.n - 1)
		self.stateSpacePlus = [i for i in range(self.m*self.n)] # full states
		self.actionSpace = {'U':-self.m, 'D':self.m, 'L':-1, 'R':1} # U: up one row, D: down one row
		self.possibleActions = ['U', 'D', 'L', 'R']
		self.agentPosition = 0

	def isTerminalState(self, state):
		"""
		find if agent is at the terminal state. It is the difference between the state space plus
		and the state space
		"""
		return state in self.stateSpacePlus and state not in self.stateSpace

	def getAgentRowAndColumn(self):
		"""
		get our agent row and column
		"""
		x = self.agentPosition // self.m
		y = self.agentPosition % self.n
		return x, y

	def setState(self, state):
		"""
		update our agent state with the new state
		empty grid is represented by 0
		occupied grid is represented by 1
		"""
		try:
			x, y = self.getAgentRowAndColumn()
			self.grid[x][y] = 0
			self.agentPosition = state
			x, y = self.getAgentRowAndColumn()
			self.grid[x][y] = 1
		except IndexError as IE:
			print(IE)
			pass
	
	def offGridMove(self, newSate, oldState):
		"""
		find out if our agent attempts to leave the grid up, down, left or right.
		get the old state and compare the action of the new state
		"""
		if newSate not in self.stateSpacePlus:
			"""
			our agent is trying to leave the grid entirely
			"""
			return True
		elif oldState % self.m == 0 and newSate % self.m == self.m - 1:
			return True
		elif oldState % self.m == self.m - 1 and newSate % self.m == 0:
			return True
		else:
			return False

	def step(self, action):
		"""
		agent movements inside or going outside grid.
		returns new state, reward, if is terminal state and debug info
		"""
		x, y = self.getAgentRowAndColumn()
		resultingState = self.agentPosition + self.actionSpace[action]

		reward = -1 if not self.isTerminalState(resultingState) else 0

		if not self.offGridMove(resultingState, self.agentPosition):
			"""
			not going off grid, set the state to the resulting state
			"""
			self.setState(resultingState)
			return resultingState, reward, self.isTerminalState(self.agentPosition), None

		else:
			"""
			agent going off grid, DO NOT SET THE NEW STATE
			"""
			return self.agentPosition, reward, self.isTerminalState(self.agentPosition), None

	def reset(self):
		"""
		reset our environment after each episode
		returns agent position zero
		"""
		self.agentPosition = 0
		self.grid = np.zeros((self.m * self.n))
		return self.agentPosition

	def render(self):
		"""
		output our environment to terminal/console for debug
		"""
		print('-'*50)
		for row in self.grid:
			for col in row:
				if col == 0: # empty square
					print('-', end='\t')
				elif col ==1: # occupied by agent
					print('x', end='\t')
			print('\n')
		print('-'*50)

	def actionSpaceSample(self):
		"""
		return random choice from list of possible actions
		"""
		return np.random.choice(self.possibleActions)

def maxAction(Q, state, actions):
	"""
	return max action of the Q-Learning Algorithm
	argmax returns the index of the max action
	"""
	values = np.array([Q[state, a] for a in actions])
	action = np.argmax(values)
	return actions[action]

def main():
	magicSquares = {18:54, 63:14}
	env = GridWorld(9, 9)
	ALPHA = 0.1 # learning rate
	GAMMA = 1.0 # discount factor
	EPS = 1.0 # epsilon
	Q = {}
	for state in env.stateSpacePlus:
		for action in env.possibleActions:
			Q[state, action] = 0
	numGames = 50000
	totalRewards = np.zeros(numGames)
	env.render()

	for i in range(numGames):
		if i % 5000 == 0:
			print('starting game', i)
		done = False
		epRewards = 0
		observation = env.reset()

		while not done:
			rand = np.random.random()
			action = maxAction(Q, observation, env.possibleActions) if rand < (1 - EPS) \
				else env.actionSpaceSample()

			observation_, reward, done, info = env.step(action)
			epRewards += reward

			action_ = maxAction(Q, observation_, env.possibleActions)

			Q[observation, action] = (Q[observation, action] + ALPHA * 
									(reward + GAMMA * Q[observation_, action_] - Q[observation, action]))
			
			observation = observation_

		if EPS - 2 / numGames > 0:
			EPS -= 2
		else:
			EPs = 0

		totalRewards[i] = epRewards

	plt.plot(totalRewards)
	plt.show()

if __name__=="__main__":
	main()
