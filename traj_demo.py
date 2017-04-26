from itertools import product

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arrow, Circle
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
import matplotlib.patches as patches

'''
Trajectory visualization demo
Mark Ho 2017


'''

def visualize_trajectory(axis, traj, 
						 jitter_mean=0,
						 jitter_var = .1, endpoint_jitter = False,
						 color = 'black', **kwargs):
	'''
	traj is a list of (state, action) pairs
	'''
	if len(traj) == 2:
		p0 = tuple(np.array(traj[0][0])+.5)
		p2 = tuple(np.array(traj[1][0])+.5)
		p1 = np.array([(p0[0]+p2[0])/2, (p0[1]+p2[1])/2])+np.random.normal(0, jitter_var, 2)
		if endpoint_jitter:
			p0 = tuple(np.array(p0)+np.random.normal(jitter_mean, jitter_var, 2))
			p1 = tuple(np.array(p1)+np.random.normal(jitter_mean, jitter_var, 2))
		segments = [[p0, p1, p2],]
	elif (len(traj) == 3) and (traj[0][0] == traj[2][0]):
		p0 = tuple(np.array(traj[0][0])+.5)
		p2 = tuple(np.array(traj[1][0])+.5)
		if abs(p0[0] - p2[0]) > 0: #horizontal
			jitter = np.array([0, np.random.normal(jitter_mean, jitter_var*2)])
			p2 = p2 - np.array([.25, 0])
		else: #vertical
			jitter = np.array([np.random.normal(jitter_mean, jitter_var*2), 0])
			p2 = p2 - np.array([0, .25])
		p1 = p2 + jitter
		p3 = p2 - jitter
		segments = [[p0, p1, p2], [p2, p3, p0]]
	else:
		state_coords = [tuple(np.array(s)+.5+np.random.normal(jitter_mean, jitter_var, 2)) for s, a in traj]
		if not endpoint_jitter:
			state_coords[0] = tuple(np.array(traj[0][0])+.5)
			state_coords[-1] = tuple(np.array(traj[-1][0])+.5)
		join_point = state_coords[0]
		segments = []
		for i, s in enumerate(state_coords[1:-1]):
			i += 1
			ns = state_coords[i+1]

			segment = []
			segment.append(join_point)
			segment.append(s)
			if i < len(traj)-2:
				join_point = tuple(np.mean([s, ns], axis=0))
				segment.append(join_point)
			else:
				segment.append(ns)
			segments.append(segment)			
	for segment in segments:
		codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
		path = Path(segment, codes)
		patch = patches.PathPatch(path, facecolor='none', capstyle='butt', edgecolor=color, **kwargs)
		axis.add_patch(patch)

def visualize_states(ax=None, states=None, 
					 tile_color=None, **kwargs):
	'''
	tile_color : a dictionary from tiles (states) to colors
	'''
	if tile_color is None:
		tile_color = {}

	if ax == None:
		fig = plt.figure()
		ax = fig.add_subplot(111)
	#plot squares
	for s in states:
		if s == (-1, -1):
			continue
		square = Rectangle(s, 1, 1, color=tile_color.get(s, 'white'), ec='k', lw=2)
		ax.add_patch(square)

	ax.axis('off')
	ax.set_xlim(-0.1, 1+max([s[0] for s in states])+.1)
	ax.set_ylim(-0.1, 1+max([s[1] for s in states])+.1)
	ax.axis('scaled')

	return ax
	
if __name__ == '__main__':
	states = list(product(range(5), range(5)))
	ax = visualize_states(states=states)
	traj = [((0,0),'>'), ((1,0),'^'), ((1,1), '>'), ((1,2), '^'), 
			((2,2),'>'), ((3,2), '>'), ((4,2),'^'), ((4,3), '^'), ((4,4), 'x')]
	visualize_trajectory(ax, traj)
	plt.show()