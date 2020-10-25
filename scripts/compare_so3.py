"""
=========================================
Comparison of Manifold Learning methods
=========================================

An illustration of dimensionality reduction on the S-curve dataset
with various manifold learning methods.

For a discussion and comparison of these algorithms, see the
:ref:`manifold module page <manifold>`

For a similar example, where the methods are applied to a
sphere dataset, see :ref:`sphx_glr_auto_examples_manifold_plot_manifold_sphere.py`

Note that the purpose of the MDS is to find a low-dimensional
representation of the data (here 2D) in which the distances respect well
the distances in the original high-dimensional space, unlike other
manifold-learning algorithms, it does not seeks an isotropic
representation of the data in the low-dimensional space.
"""

# Author: Jake Vanderplas -- <vanderplas@astro.washington.edu>

print(__doc__)

from collections import OrderedDict
from functools import partial
from time import time
import sys
import os
import numpy as np
from scipy.spatial.transform import Rotation as R

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn import manifold, datasets
import sammon

# Next line to silence pyflakes. This import is needed.
Axes3D

n_points = 1000
# X, color = datasets.make_swiss_roll(n_points, 0.0, random_state=0)
rot_axis = [np.array([1,1,-1]) / 3**0.5, np.array([-1,1,1]) / 3**0.5, np.array([1,-1,1]) / 3**0.5, np.array([1,1,1]) / 3**0.5]

for axis_num in range(1, 5):
    n_points = (n_points // axis_num) * axis_num
    theta = np.linspace(0.0, 2* np.pi, n_points // axis_num)
    color = np.linspace(0, 1, n_points)
    rot_vecs = np.vstack([np.outer(theta, rot_axis[i]) for i in range(axis_num)])

    rots = R.from_rotvec(rot_vecs)
    X = np.reshape(rots.as_matrix(), (-1, 9))

    n_neighbors = 10
    n_components = 2

    # Create figure
    fig = plt.figure(figsize=(15, 8))
    fig.suptitle("Manifold Learning with %i points, %i neighbors"
                % (1000, n_neighbors), fontsize=14)

    # Add 3d scatter plot
    ax = fig.add_subplot(231, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap=plt.cm.Spectral)
    ax.view_init(4, -72)

    # Set-up manifold methods
    LLE = partial(manifold.LocallyLinearEmbedding,
                n_neighbors, n_components, eigen_solver='auto')

    methods = OrderedDict()
    methods['LLE'] = LLE(method='standard')
    methods['Sammon'] = sammon.Sammon()
    # methods['Hessian LLE'] = LLE(method='hessian')
    # methods['Modified LLE'] = LLE(method='modified')
    methods['Isomap'] = manifold.Isomap(n_neighbors, n_components)
    # methods['MDS'] = manifold.MDS(n_components, max_iter=100, n_init=1)
    # methods['SE'] = manifold.SpectralEmbedding(n_components=n_components,
    #                                            n_neighbors=n_neighbors)
    methods['t-SNE'] = manifold.TSNE(n_components=n_components, init='pca',
                                    random_state=0)

    # Plot results
    for i, (label, method) in enumerate(methods.items()):
        t0 = time()
        Y = method.fit_transform(X)
        t1 = time()
        print("%s: %.2g sec" % (label, t1 - t0))
        print(2 + i + (i > 1))
        ax = fig.add_subplot(2, 3, 2 + i + (i > 1))
        ax.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
        ax.set_title("%s (%.2g sec)" % (label, t1 - t0))
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.axis('tight')

    current_script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
    output_basename = os.path.basename(os.path.splitext(__file__)[0]) + ('_{}'.format(axis_num) if axis_num > 1 else '') + '.pdf'
    output_filename = os.path.join(current_script_folder, '..', 'build', output_basename)
    fig.savefig(output_filename, bbox_inches='tight')
    # plt.show()
