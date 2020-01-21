# mandelbrot-generator

dependencies:
    -matplotlib
    -numpy

description:

-Generates an image of the mandelbrot set according to the parameters in config.py, color is determined by how quickley the generating function diverges (black is chosen for convergence to increse contrast,dark blue is maximum divergence). 

-Right clicking anywhere on the image will re-render it zoomed into the point of clicking while maintaining the same resolution, this however does not change the number of iterations. 

-Multiprocessing is used to increase the image rendering time, it is highly recommended for resolutions 500x500 and up and for high iteration counts. 
