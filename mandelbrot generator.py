def clickZoom(event):
    if event.button==3:
        zoomCenter=(event.xdata,event.ydata)
        sideLength=(state.xBounds[1]-state.xBounds[0])*config.newWindowSize
        x1,x2,y1=findSquare(zoomCenter,sideLength)
        y2=y1+sideLength

        #updates state
        state.xBounds=(x1,x2)
        state.yBounds=(y1,y1+sideLength)

        state.xVals=linspace(x1,x2,state.resolution[0])
        state.yVals=linspace(y1,y2,state.resolution[1])

        #generates new mandelbrot
        createColorMandelbrot(config,state)

def findSquare(squareCenter,sideLenght):
    x1=squareCenter[0]-sideLenght/2
    x2=squareCenter[0]+sideLenght/2

    y1=squareCenter[1]-sideLenght/2
    return(x1,x2,y1)

def iterate(a,z):
    nextA=(a+z)**2
    return(nextA)

#returns the number of iterations until it detects divergence
def didConvergeAtZWithRate(z,iterations,threshold):
    a=0
    #iterates a until modulus a is greather than the
    #threshold, or until it reaches the max number of iterations
    for i in range(1,iterations+1):
        a=iterate(a,z)
        magA=(a.real)**2+(a.imag)**2
        if magA>threshold:
            return(i)
    return(0)

#used by pool.starmap() for multiprocessing
def calculateImageArrayRow(yIndex,imageRow,state):
    print(yIndex)
    iterations=state.iterations
    threshold=state.threshold

    for xIndex in range(0,state.resolution[1]):
        z=state.xVals[xIndex]+state.yVals[yIndex]*1j
        iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
        imageRow[xIndex]=iterationsTillDivergence/iterations
    return(imageRow)

def populateImageArray(imageArray,config,state):
    resolution=config.resolution
    iterations=config.iterations
    threshold=config.threshold

    if config.enableMultiProcessing:

        p=Pool(config.processesUsed)
        rowsPerChunk=int(ceil(resolution[0]/(8*config.processesUsed)))
        iterable=[]
        for yIndex,row in enumerate(imageArray):
            iterable.append((yIndex,row,state))
        imageArray=p.starmap(calculateImageArrayRow,iterable,chunksize = rowsPerChunk)

        p.close()
        p.join()
    
    else:
        for xIndex in range(0,resolution[0]):
            print(xIndex)
            for yIndex in range(0,resolution[1]):
                z=state.xVals[xIndex]+(state.yVals[yIndex])*1j
                #note, array indices are flipped because arrays are silly
                #also note each entry of the image array is 1/(the number of iterations until divergence)
                iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
                imageArray[yIndex,xIndex]=iterationsTillDivergence/iterations
    return(imageArray)

def createColorMandelbrot(config,state):
    resolution=config.resolution
    imageArray=zeros((resolution[0], resolution[1]), dtype=float)
    imageArray=populateImageArray(imageArray,config,state)
    plt.close()
    fig=plt.figure()
    fig.canvas.mpl_connect('button_press_event', clickZoom)
    ax=fig.add_subplot(111)
    x1,x2=state.xBounds[0],state.xBounds[1]
    y1,y2=state.yBounds[0],state.yBounds[1]

    ax.imshow(imageArray,origin='lower',cmap='gnuplot', aspect='equal', interpolation='nearest',extent=[x1,x2,y1,y2])
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.title('Right Click To Zoom')

    manager = plt.get_current_fig_manager()
    if config.enableFullScreen:
        manager.full_screen_toggle()
    
    plt.show()

def main(config,state):
    createColorMandelbrot(config,state)


if __name__ == "__main__":
    from numpy import linspace,zeros,array
    from math import ceil
    from multiprocessing import Pool
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from config import Config
    from state import State

    config=Config()
    state=State()
    state.getConfigData(config)

    main(config,state)