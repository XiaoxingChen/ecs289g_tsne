import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import sys
import os
import numpy as np
from scipy.spatial.transform import Rotation as R

def cubify_cube_definition(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]
    start = cube_definition_array[0]
    length_decider_vector = cube_definition_array[1] - cube_definition_array[0]   
    length = np.linalg.norm(length_decider_vector)

    rotation_decider_vector = (cube_definition_array[2] - cube_definition_array[0])
    rotation_decider_vector = rotation_decider_vector / np.linalg.norm(rotation_decider_vector) * length

    orthogonal_vector = np.cross(length_decider_vector, rotation_decider_vector)
    orthogonal_vector = orthogonal_vector / np.linalg.norm(orthogonal_vector) * length

    orthogonal_length_decider_vector = np.cross(rotation_decider_vector, orthogonal_vector)
    orthogonal_length_decider_vector = (
        orthogonal_length_decider_vector / np.linalg.norm(orthogonal_length_decider_vector) * length)

    final_points = [
        tuple(start),
        tuple(start + orthogonal_length_decider_vector),
        tuple(start + rotation_decider_vector),
        tuple(start + orthogonal_vector)        
    ]

    return final_points


def cube_vertices(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]

    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    return points


def get_bounding_box(points): 
    x_min = np.min(points[:,0])
    x_max = np.max(points[:,0])
    y_min = np.min(points[:,1])
    y_max = np.max(points[:,1])
    z_min = np.min(points[:,2])
    z_max = np.max(points[:,2])

    max_range = np.array(
        [x_max-x_min, y_max-y_min, z_max-z_min]).max() / 2.0

    mid_x = (x_max+x_min) * 0.5
    mid_y = (y_max+y_min) * 0.5
    mid_z = (z_max+z_min) * 0.5

    return [
        [mid_x - max_range, mid_x + max_range],
        [mid_y - max_range, mid_y + max_range],
        [mid_z - max_range, mid_z + max_range]
    ]


def plot_cube(cube_definition, ax):
    points = cube_vertices(cube_definition)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

    faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
    faces.set_facecolor((0,0,1,0.1))

    ax.add_collection3d(faces)

    bounding_box = get_bounding_box(points)

    ax.set_xlim(bounding_box[0])
    ax.set_ylim(bounding_box[1])
    ax.set_zlim(bounding_box[2])

    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    # ax.set_aspect('equal')
    plt.axis('off')
    ax.grid(False)
    ax.set_title("Rotation in 3D space")

    ax.view_init(32, -80)
    ax.dist = 6

def plot_4_circles(ax):
    n_points = 1000
    axis_num = 4
    rot_axis = [np.array([1,1,-1]) / 3**0.5, np.array([-1,1,1]) / 3**0.5, np.array([1,-1,1]) / 3**0.5, np.array([1,1,1]) / 3**0.5]
    n_points = (n_points // axis_num) * axis_num
    theta = np.linspace(0.0, 2* np.pi, n_points // axis_num)
    color = np.linspace(0, 1, n_points)
    rot_vecs = np.vstack([np.outer(theta, rot_axis[i]) for i in range(axis_num)])

    rots = R.from_rotvec(rot_vecs)
    X = np.reshape(rots.as_matrix(), (-1, 9))

    n_neighbors = 10
    n_components = 2
    
    plt.axis('off')
    ax.set_title("Orientations")
    ax.grid(False)
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap=plt.cm.Spectral)
    ax.view_init(-9, 164)
    ax.dist = 7


cube_definition = cubify_cube_definition([(0,0,0), (0,3,0), (1,1,0.3)])

fig = plt.figure(figsize=[12,6])
ax1 = fig.add_subplot(121, projection='3d')
plot_cube(cube_definition, ax1)
ax2 = fig.add_subplot(122, projection='3d')
plot_4_circles(ax2)

current_script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
output_filename = os.path.join(current_script_folder, '..', 'build', os.path.basename(os.path.splitext(__file__)[0]) + '.pdf')
fig.savefig(output_filename, bbox_inches='tight')
print("replot {}".format(output_filename))
# plt.show()