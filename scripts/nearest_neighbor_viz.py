import matplotlib.pyplot as plt
import os
import sys
import numpy as np

if __name__ == "__main__":
    np.set_printoptions(precision=5, linewidth=np.inf)
    
    plt.figure(figsize=[5,5])
    # plt.grid(1)
    
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')

    t = np.linspace(0, 2 * np.pi, 50)
    c1 = np.array([np.cos(t),np.sin(t)])

    # rands = np.random.random((2, 10))
    rands = [[0.97639865, 0.96300587, 0.72383031, 0.11606981, 0.7835818 ,
        0.8958146 , 0.32430413, 0.51036209, 0.74356518, 0.20813713,
        0.31616536, 0.48188347, 0.01459113, 0.25379224, 0.47339893,
        0.46119536, 0.9749884 , 0.46394353, 0.26278203, 0.92387824,
        0.61546118, 0.82863059, 0.53076001, 0.36814272, 0.42720543,
        0.57554356, 0.75342694, 0.87083798, 0.40037604, 0.67180655],
       [0.64920378, 0.52153716, 0.86492079, 0.91107421, 0.45638313,
        0.21304132, 0.63604565, 0.3185487 , 0.94780181, 0.59155249,
        0.53867041, 0.60913379, 0.36523386, 0.2950856 , 0.49221367,
        0.15060697, 0.53288702, 0.97068344, 0.41746204, 0.02999611,
        0.43333559, 0.60626046, 0.96200292, 0.4245835 , 0.36799172,
        0.55825821, 0.06033996, 0.93213289, 0.79225726, 0.62428875]]

    plt.plot([0.5], [0.5], 'go', markersize=8)

    plt.plot(rands[0], rands[1], 'bo', markersize=5)
    plt.xlim([0.2,.8])
    plt.ylim([0.2,.8])

    plt.plot(c1[0] * 0.125 + 0.5, c1[1] * 0.125 + 0.5)
    plt.plot(c1[0] * 0.235 + 0.5, c1[1] * 0.235 + 0.5)
    
    plt.annotate('k = 3', xy=(0.48, 0.63))
    plt.annotate('k = 10', xy=(0.48, 0.75))
    # plt.plot(0, -0.1)
    # plt.legend()
    # fig = plt.gcf()
    # fig.savefig('__pycache__/{}.svg'.format(os.path.splitext(__file__)[0]))
    # plt.show()
    current_script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
    output_filename = os.path.join(current_script_folder, '..', 'build', os.path.basename(os.path.splitext(__file__)[0]) + '.pdf')
    fig = plt.gcf()
    fig.savefig(output_filename, bbox_inches='tight')