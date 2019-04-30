from numpy import linspace,zeros,array
from multiprocessing import Pool
import matplotlib.pyplot as plt
from config import config
#these must be defined on main scope due to the inability to pass multiple inputs in pool.map()
xVals=linspace(-2,1,config.resolution[0])
yVals=linspace(-3/2,3/2,config.resolution[1])

def iterate(a,z):
    nextA=(a+z)**2
    return(nextA)

def didConvergeAtZ(z,iterations,threshold):
    a=0
    #iterates a until modulus a is greather than the
    #threshold, or until it reaches the max number of iterations
    for i in range(1,iterations+1):
        a=iterate(a,z)
        magA=(a.real)**2+(a.imag)**2
        if magA>threshold:
            return(False)
    return(True)

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
def calculateImageArrayColumn(tup):
    iterations=config.iterations
    threshold=config.threshold
    yIndex=tup[0]
    imageColumn=tup[1]
    print(yIndex)
    for xIndex in range(0,config.resolution[1]):
        z=xVals[xIndex]+yVals[yIndex]*1j
        iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
        imageColumn[xIndex]=iterationsTillDivergence/iterations
    return(imageColumn)

def populateBoolArray(boolArray,resolution,iterations,threshold):
    #x and y value are orginized from least to greatest 
    for xIndex in range(0,resolution[0]):
        print(xIndex)
        for yIndex in range(0,resolution[1]):
            z=xVals[xIndex]+(yVals[yIndex])*1j
            #note, array indices are flipped because arrays are silly
            boolArray[yIndex,xIndex]=didConvergeAtZ(z,iterations,threshold)
    return(boolArray)

def populateImageArray(imageArray,resolution,iterations,threshold):
    #x and y value are orginized from least to greatest 
    if config.enableMultiProcessing:
        p=Pool(config.coresAllocated)
        imageArray=array(p.map(calculateImageArrayColumn,enumerate(imageArray)))
    else:
        for xIndex in range(0,resolution[0]):
            print(xIndex)
            for yIndex in range(0,resolution[1]):
                z=xVals[xIndex]+(yVals[yIndex])*1j
                #note, array indices are flipped because arrays are silly
                #also note each entry of the image array is 1/(the number of iterations until divergence)
                iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
                imageArray[yIndex,xIndex]=iterationsTillDivergence/iterations
    return(imageArray)

def createBoolMandelbrot(resolution,iterations,threshold):
    boolArray=zeros((resolution[0], resolution[1]), dtype=bool)
    boolArray=populateBoolArray(boolArray,resolution,iterations,threshold)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.imshow(boolArray,origin='lower', aspect='equal', interpolation='nearest')

    plt.show()

def createColorMandelbrot(resolution,iterations,threshold):
    imageArray=zeros((resolution[0], resolution[1]), dtype=float)
    imageArray=populateImageArray(imageArray,resolution,iterations,threshold)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.imshow(imageArray,origin='lower',cmap='gnuplot', aspect='equal', interpolation='nearest')

    #plt.colorbar()
    #pickle.dump(fig, open('mandelbrot','wb'))
    plt.show()

def main():
    if config.type=='bool':
        createBoolMandelbrot(config.resolution,config.iterations,config.threshold)
    
    elif config.type=='color':
        createColorMandelbrot(config.resolution,config.iterations,config.threshold)
    
    else:
        print('invalid mandelbrot type')

if __name__ == "__main__":
    main()