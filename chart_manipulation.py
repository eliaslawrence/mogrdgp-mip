#Author: Elias Lawrence

import matplotlib.pyplot as plt

def scatter(ax, points, color, text, number):
	for i, p in enumerate(points):
		ax.scatter((p[0]), (p[1]), marker="o", color=color, s=15)

		if number:
			ax.text((p[0]), (p[1]), str(p[1]))
		else:		
			ax.text((p[0]), (p[1]), "${}_{}$".format(text, i))	

