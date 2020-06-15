import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import numpy as np
from Time import Time
from Student import Student, Schedule


class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, agents, CURRENT_TIME):
        self.numpoints = 10
        self.agents = agents
        self.CURRENT_TIME = CURRENT_TIME
        self.stream = self.data_stream()
        img = cv2.imread("map.png")
        
        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=200, 
                                          init_func=self.setup_plot, blit=False)
        plt.imshow(img, zorder=0,  extent=[0, 16000, 0, 16000])
        self.ani.save('scatter_animation.mp4', writer='ffmpeg', fps=30) #/save as .mp4

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y= next(self.stream).T
        self.scat = self.ax.scatter(x, y, vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        self.ax.axis([0, 16000, 0, 16000])
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def data_stream(self):
        """Generate a random walk (brownian motion). Data is scaled to produce
        a soft "flickering" effect."""
        xy = np.array([agent.currentPosition for agent in self.agents])
        print(xy)
        #xy = (np.random.random((self.numpoints, 2))-0.5)*10
        #print(xy)
        while True:
            xy = np.array([agent.currentPosition for agent in self.agents])
            print(xy)
            #xy += 0.3 * (np.random.random((self.numpoints, 2)) - 0.5)
            #print(xy)
            yield np.c_[xy[:,0], xy[:,1]]

    def update(self, i):
        """Update the scatter plot."""
        self.CURRENT_TIME = Time.addMinutes(self.CURRENT_TIME, 1)
        print(self.CURRENT_TIME)
        for agent in self.agents:
            agent.Action(self.CURRENT_TIME)
        data = next(self.stream)

        # Set x and y data...
        self.scat.set_offsets(data[:, :2])
        # Set sizes...
        #self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
        # Set colors..

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    
if __name__ == '__main__':
    CURRENT_TIME = '07:50'
    agents = []
    for i in range(10):
        student = Student()
        while Time.compare(student.schedule.destTimes[0], '>=', '09:10'):
            student = Student()
        agents.append(student)
    a = AnimatedScatter(agents, CURRENT_TIME)
    plt.show()