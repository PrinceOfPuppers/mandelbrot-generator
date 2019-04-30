class config:
    def __init__(self):
        #type is either color or bool
        self.type="color"
        self.resolution=(100,100)
        #iterations and resolution are best considered togeather ie 5000x5000 needs 
        #an iteration number greather than 30
        self.iterations=60
        #the treshold chosen from a reccomendation on wikipedia
        self.threshold=4

config=config()