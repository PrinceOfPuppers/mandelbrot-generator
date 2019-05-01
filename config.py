from numpy import linspace
class config:
    def __init__(self):
        #type is either color or bool
        resolution=(500,500)
        #iterations and resolution are best considered togeather ie 5000x5000 needs 
        #an iteration number greather than 30
        self.iterations=100
        self.threshold=20

        #mutiProcessing only supported for color mandelbrot
        self.enableMultiProcessing=True
        self.coresAllocated=8

        #starting screen (yUpperBound is calculated to keep it square)
        xLowerBound=-2
        xUpperBound=1

        yLowerBound=-3/2

        #after each click zoom, how big is the screen compared to last time
        self.newWindowSize=1/2

        #non adjustable
        self.resolution=resolution
        yUpperBound=yLowerBound+(xUpperBound-xLowerBound)
        self.xBounds=(xLowerBound,xUpperBound)
        self.yBounds=(yLowerBound,yUpperBound)
        self.xVals=linspace(xLowerBound,xUpperBound,resolution[0])
        self.yVals=linspace(yLowerBound,yUpperBound,resolution[1])