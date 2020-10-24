from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
import os
import sys

def geodesicLineOnSphere(xx, yy, zz, resolution=20, c=np.zeros(3), r=1.):
    t = np.linspace(0,1,resolution)
    eu_line = np.array([t * xx[0] + (1-t)*xx[1], t * yy[0] + (1-t)*yy[1], t * zz[0] + (1-t)*zz[1]])
    vec = eu_line.T - c 
    nm = np.linalg.norm(vec, axis=1)
    geodesic_line = vec / np.outer(nm, np.ones(3)) + c

    return geodesic_line.T


fig = plt.figure(figsize=[6.5,6])
ax = fig.gca(projection='3d')
# ax.set_aspect("equal")

# draw sphere
u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)

p1 = (30, 12)
p2 = (0, 6)
ax.plot_wireframe(x, y, z, alpha=0.2)

point_pair = [[x[p1], x[p2]], [y[p1], y[p2]], [z[p1], z[p2]]]

ax.scatter(*point_pair, color="g", s=40)
ax.plot3D(*point_pair)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.axis('off')

geodesic_line = geodesicLineOnSphere(point_pair[0], point_pair[1], point_pair[2])
ax.plot3D(*geodesic_line, 'r')

ax.view_init(32, -80)
ax.dist = 6

current_script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
output_filename = os.path.join(current_script_folder, '..', 'build', os.path.basename(os.path.splitext(__file__)[0]) + '.pdf')
fig.savefig(output_filename, bbox_inches='tight')
print("replot {}".format(output_filename))
# plt.show()