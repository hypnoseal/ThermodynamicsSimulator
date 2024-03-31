import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import numpy as np


class Animator:
    """
    The Animator class creates an 3D animated plot based on the input data.

    :param data: A numpy array of data to animate.
    :param start_value: The floor of the range of scalar values for the colormap.
    :param end_value: The ceiling of the range of scalar values for the colormap.
    :param interval: Delay between frames in milliseconds. Default is 100.
    """

    # Initialization method to set up parameters for the animation
    def __init__(self, data, start_value, end_value, interval=100):
        self.data = data
        self.start_value = start_value
        self.end_value = end_value
        self.interval = interval
        self.fig = None

    # Method to create the 3D plot, animate it, and save the animation as a video
    def plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        animation = FuncAnimation(self.fig, self.update_plot, frames=len(self.data), repeat=False,
                                  interval=self.interval)
        plt.show()
        animation.save('thermodynamics_simulation.mp4', writer='ffmpeg')

    # Method to update the frames for the animation
    def update_plot(self, frame):
        self.ax.cla()
        cube_state = self.data[frame]
        filled = np.ones(cube_state.shape, dtype=bool)

        colors = cm.turbo((cube_state - self.start_value) / (self.end_value - self.start_value))
        self.ax.voxels(filled, facecolors=colors, edgecolor='k')

        self.ax.set_xlim(0, cube_state.shape[0])
        self.ax.set_ylim(0, cube_state.shape[1])
        self.ax.set_zlim(0, cube_state.shape[2])

        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.zaxis.set_major_locator(MaxNLocator(integer=True))

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        plt.title(f'Time Step: {frame}')
