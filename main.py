
def clickZoom(event):
    if event.button==1:
        zoomCenter=(event.xdata,event.ydata)
        #print(zoomCenter)
        sideLength=(config.xBounds[1]-config.xBounds[0])*config.newWindowSize
        x1,x2,y1=findSquare(zoomCenter,sideLength)
        y2=y1+sideLength
        #print((x1,y1),",",(x2,y1),",",(x1,y2),",",(x2,y2))

        #updates config
        config.xBounds=(x1,x2)
        config.yBounds=(y1,y1+sideLength)

        config.xVals=linspace(x1,x2,config.resolution[0])
        config.yVals=linspace(y1,y2,config.resolution[1])

        #generates new mandelbrot
        createColorMandelbrot(config.resolution,config.iterations,config.threshold)

def findSquare(squareCenter,sideLenght):
    x1=squareCenter[0]-sideLenght/2
    x2=squareCenter[0]+sideLenght/2

    y1=squareCenter[1]-sideLenght/2
    return(x1,x2,y1)

def iterate(a,z):
    nextA=(a+z)**2
    return(nextA)

#also returns the number of iterations until it detects divergence
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

#used by pool.map() for multiprocessing
def calculateImageArrayRow(yIndex,imageRow,config):
    print(yIndex)
    iterations=config.iterations
    threshold=config.threshold

    for xIndex in range(0,config.resolution[1]):
        z=config.xVals[xIndex]+config.yVals[yIndex]*1j
        iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
        imageRow[xIndex]=iterationsTillDivergence/iterations
    return(imageRow)

def populateImageArray(imageArray,resolution,iterations,threshold):
    #x and y value are orginized from least to greatest 
    if config.enableMultiProcessing:

        p=Pool(config.coresAllocated)
        rowsPerChunk=int(ceil(resolution[0]/(8*config.coresAllocated)))
        iterable=[]
        for yIndex,row in enumerate(imageArray):
            iterable.append((yIndex,row,config))
        imageArray=p.starmap(calculateImageArrayRow,iterable,chunksize = rowsPerChunk)

        p.close()
        p.join()
    else:
        for xIndex in range(0,resolution[0]):
            print(xIndex)
            for yIndex in range(0,resolution[1]):
                z=config.xVals[xIndex]+(config.yVals[yIndex])*1j
                #note, array indices are flipped because arrays are silly
                #also note each entry of the image array is 1/(the number of iterations until divergence)
                iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
                imageArray[yIndex,xIndex]=iterationsTillDivergence/iterations
    return(imageArray)

def createColorMandelbrot(resolution,iterations,threshold):
    imageArray=zeros((resolution[0], resolution[1]), dtype=float)
    imageArray=populateImageArray(imageArray,resolution,iterations,threshold)
    plt.close()
    fig=plt.figure()
    cid = fig.canvas.mpl_connect('button_press_event', clickZoom)
    ax=fig.add_subplot(111)
    x1,x2=config.xBounds[0],config.xBounds[1]
    y1,y2=config.yBounds[0],config.yBounds[1]

    ax.imshow(imageArray,origin='lower',cmap='gnuplot', aspect='equal', interpolation='nearest',extent=[x1,x2,y1,y2])
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.show()

def main():
    createColorMandelbrot(config.resolution,config.iterations,config.threshold)


if __name__ == "__main__":
    from numpy import linspace,zeros,array
    from math import ceil
    from multiprocessing import Pool
    import matplotlib.pyplot as plt
    from config import config

    config=config()
    main()