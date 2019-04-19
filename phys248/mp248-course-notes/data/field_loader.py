import sympy as sp
import numpy as np
from scipy import integrate as INT
from sympy.utilities.autowrap import ufuncify
import itertools as it
from ipywidgets import FloatProgress
from IPython.display import display

## Takes four arguments, 
##  1) the parametrization packet F, which is a 3-element list. F=[f,var,dom]
##     f is a Sympy vector-valued function of the variables in the list var.
##     dom is a list of lists, describing the domain of f.  If F is a two
##     variables function with domain [a,b]x[c,d] then dom would be
##     dom = [[a,b],[c,d]]
##  2) the current packet Ipb which is a sympy vector field. This is also a function
##    of the variables of var, and should be an n-tuple where var has n elements.
##    Ipb = [1,0] would represent the d()/dx i.e. the 1st unit vector field.
##  3) the lattice of coordinates to compute magnetic fields at, LAT. 
##     this is a 3-element list of lists of x, y, z coordinates
##     for the lattice. 
##  4) flow is a 2-element list, flow=[fs,fn]
##     with fs=[flow step size, fn=number of steps] in an Euler approx.
## 
## flowlines returns a pair 1) the flowlines and 2) a callable version of F, to help with
##  plotting.
def flowLines(F, Ipb, LAT, flow):
    f = F[0]  ## sympy function, matrix valued. 
    k = len(F[1]) ## number of parameters to f. F[1] is the variable names.
    ## F[2] is the integration bounds. 
    
    Df = sp.zeros(3,k)
    for i in range(k):
        Df[:,i] = sp.diff(f, F[1][i])
    Cf = sp.sqrt( (Df.transpose()*Df).det() ).simplify()
    ## Cf is the length/area/volume distortion of f. 
    
    x,y,z = sp.symbols('x y z')
    P = sp.Matrix([x,y,z])
    ## we have to push I through Df to get the current vector field. 
    I = Df*Ipb
    den = sp.Matrix(f-P)
    ITG = I.cross(den)
    den = den.dot(den)**(3/2)
    ITG = (ITG/den)
    
    ## let's make an entire routine that does Euler's method callable? 
    ## this is possibly something to experiment with, the level of abstraction.
    ## we could also just make the integration command callable. 
    ITGc = [ufuncify(F[1]+[x,y,z], ITG[i,0]) for i in range(3)]
 
    ## compile the curve as well, as we need to check distances
    C = [ufuncify(F[1], F[0][i,0]) for i in range(3)]
    
    ## loop running through the lattice [X,Y,Z]=LAT computing flowlines at those 
    ##  coordinates.
    retval = []
    fp = FloatProgress(min=0, max=100, description="Flowlines");     
    display(fp); ## progrss indicator

    count=0; totc = LAT[0].shape[0]*LAT[0].shape[1]*LAT[0].shape[2];
    for i,j,k in it.product(range(LAT[0].shape[0]), range(LAT[0].shape[1]), 
                            range(LAT[0].shape[2])):
        # TODO: let's throw in a basic check to see if this starting coordinate
        #  is too close to the curve. 
        errFlag = False
        flowline = [ [LAT[0][i,j,k]], [LAT[1][i,j,k]], [LAT[2][i,j,k]] ]
        for s in range(flow[1]):
            dp = [INT.nquad(ITGc[l], F[2], 
                            args=(flowline[0][-1], flowline[1][-1], flowline[2][-1]),
                            opts=[{'epsrel' : 0}, {'epsabs' : 1e-3}])[0] for l in range(3)]
            ## here is a primitive check to see if our lattice point is too close to
            ## the curve.  Should be replaced with something more sophisticated... later.
            ldp = np.sqrt(sum([crd**2 for crd in dp]))
                    
            if (ldp > 1e+8):
                errFlag = True
                break
            ## assemble our flowline
            for l in range(3):
                flowline[l].append(flowline[l][-1]+flow[0]*dp[l]/ldp)
        count+=1
        fp.value = int(100*count/totc)

        ## let's not build the flow line if ldp is too large. 
        if errFlag == False:
            retval.append(flowline)
    fp.close()

    return retval, C