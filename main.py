from numpy import linspace,zeros
import matplotlib.pyplot as plt
import pickle

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

def populateBoolArray(boolArray,resolution,xVals,yVals,iterations,threshold):
    #x and y value are orginized from least to greatest 
    for xIndex in range(0,resolution[0]):
        for yIndex in range(0,resolution[1]):
            print(xIndex,yIndex)
            z=xVals[xIndex]+(yVals[yIndex])*1j
            #note, array indices are flipped because arrays are silly
            boolArray[yIndex,xIndex]=didConvergeAtZ(z,iterations,threshold)
    return(boolArray)

def populateImageArray(imageArray,resolution,xVals,yVals,iterations,threshold):
    #x and y value are orginized from least to greatest 
    for xIndex in range(0,resolution[0]):
        for yIndex in range(0,resolution[1]):
            print(xIndex,yIndex)
            z=xVals[xIndex]+(yVals[yIndex])*1j
            #note, array indices are flipped because arrays are silly
            #also note each entry of the image array is 1/(the number of iterations until divergence)
            iterationsTillDivergence=didConvergeAtZWithRate(z,iterations,threshold)
            imageArray[yIndex,xIndex]=iterationsTillDivergence/iterations
    return(imageArray)

def createBoolMandelbrot(resolution,iterations,threshold):
    xVals=linspace(-2,1,resolution[0])
    yVals=linspace(-3/2,3/2,resolution[1])

    boolArray=zeros((resolution[0], resolution[1]), dtype=bool)
    boolArray=populateBoolArray(boolArray,resolution,xVals,yVals,iterations,threshold)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.imshow(boolArray,origin='lower', aspect='equal', interpolation='nearest')

    plt.show()

def createColorMandelbrot(resolution,iterations,threshold):
    xVals=linspace(-2,1,resolution[0])
    yVals=linspace(-3/2,3/2,resolution[1])

    imageArray=zeros((resolution[0], resolution[1]), dtype=float)
    imageArray=populateImageArray(imageArray,resolution,xVals,yVals,iterations,threshold)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.imshow(imageArray,origin='lower',cmap='gnuplot', aspect='equal', interpolation='nearest')

    #plt.colorbar()
    #pickle.dump(fig, open('mandelbrot','wb'))
    plt.show()


resolution=(10000,10000)
#iterations and resolution are best considered togeather ie 5000x5000 needs 
#an iteration number greather than 30
iterations=60
#the treshold chosen from a reccomendation on wikipedia
threshold=4

#createBoolMandelbrot(resolution,iterations,threshold)
createColorMandelbrot(resolution,iterations,threshold)