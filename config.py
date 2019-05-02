from numpy import linspace
from multiprocessing import cpu_count
class Config:
    def __init__(self):
        self.resolution=(800,800)
        #iterations and resolution are best considered togeather ie 5000x5000 needs 
        #an iteration number greather than 30
        self.iterations=80
        self.threshold=20

        self.enableFullScreen=True

        #mutiProcessing only supported for color mandelbrot
        self.enableMultiProcessing=True

        #the number of processes spawned is determined by cpu count, change if you wish
        self.processesUsed=cpu_count()

        #starting screen (yUpperBound is calculated to keep it square)
        xLowerBound=-2
        xUpperBound=1

        yLowerBound=-3/2

        #after each click zoom, how big is the screen compared to last time
        self.newWindowSize=1/2

        #non adjustable
        yUpperBound=yLowerBound+(xUpperBound-xLowerBound)
        self.xInitalBounds=(xLowerBound,xUpperBound)
        self.yInitalBounds=(yLowerBound,yUpperBound)