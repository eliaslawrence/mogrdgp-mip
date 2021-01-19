#Author: Elias Lawrence

import matplotlib.pyplot as plt

def scatter(ax, points, color, character):
	for i, p in enumerate(points):
	    ax.scatter((p[0]), (p[1]), marker="o", color=color, s=15)
	    ax.text((p[0]), (p[1]), "${}_{}$".format(character, i))	

