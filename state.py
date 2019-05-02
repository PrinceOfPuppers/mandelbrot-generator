from numpy import linspace
class State:
    def __init__(self):
        #starting screen (yUpperBound is calculated to keep it square)
        xLowerBound=-2
        xUpperBound=1

        yLowerBound=-3/2

        #non adjustable
        yUpperBound=yLowerBound+(xUpperBound-xLowerBound)
        self.xBounds=(xLowerBound,xUpperBound)
        self.yBounds=(yLowerBound,yUpperBound)
    
    def getConfigData(self,config):
        resolution=config.resolution

        #state is given access to these 3 so we dont have to pass both state and config to every process in multiprocessing starmap
        self.resolution=resolution
        self.iterations=config.iterations
        self.threshold=config.threshold
        
        xLowerBound,xUpperBound=config.xInitalBounds[0],config.xInitalBounds[1]
        yLowerBound,yUpperBound=config.yInitalBounds[0],config.yInitalBounds[1]

        self.xVals=linspace(xLowerBound,xUpperBound,resolution[0])
        self.yVals=linspace(yLowerBound,yUpperBound,resolution[1])