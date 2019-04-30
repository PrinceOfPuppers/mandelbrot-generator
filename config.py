class config:
    def __init__(self):
        #type is either color or bool
        self.type="color"
        self.resolution=(1000,1000)
        #iterations and resolution are best considered togeather ie 5000x5000 needs 
        #an iteration number greather than 30
        self.iterations=100
        self.threshold=10
        self.enableMultiProcessing=True
        self.coresAllocated=6
        xBounds=(-2,1)
        yLowerBound=-3/2
        self.xBounds=xBounds
        self.yBounds=(yLowerBound,yLowerBound+(xBounds[1]-xBounds[0]))

config=config()