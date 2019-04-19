import sympy as sp
import numpy as np
import itertools as it
from ipywidgets import FloatProgress


## This routine generates the data for 
## a (kp,kq)-torus knot

## refine subdivides mesh along length of torus knot
## segm is the meridional subdivision along the knot
## tR is the major radius of the torus that the knot is drawn on
## tr is the minor radius

## returns a numpy ndarray that is of dimensions (dim1,dim2, 3)
## the final 3, i.e. this is three 2-dimensional grids, giving
## the x,y and z coordinates of the surface of the torus.

def torus_dat(kp, kq, refine=300, segm=40, tR=1.6, tr=0.6):
    spt, spp, spq, spr, spR = sp.symbols("t p q r R", real=True)

    c = sp.Matrix([(spR+spr*sp.cos(2*sp.pi*spq*spt))*sp.cos(2*sp.pi*spp*spt),\
         (spR+spr*sp.cos(2*sp.pi*spq*spt))*sp.sin(2*sp.pi*spp*spt),\
          spr*sp.sin(2*sp.pi*spq*spt)])

    dc = sp.Matrix([sp.diff(x,spt) for x in c]) # derivative
    ldc = sp.sqrt(sum( [ x**2 for x in dc ] )).simplify() # speed
    udc = dc/ldc

    ## 2nd order
    kc = sp.Matrix([sp.diff(x,spt) for x in udc]) # curvature vector
    ks = sp.sqrt(sum( [ x**2 for x in kc])) # curvature scalar
    ukc = kc/ks # unit curvature vector

    ## bi-normal
    bnc = udc.cross(ukc) # cross of unit tangent and unit curvature.

    ## the parametrization of the boundary of the width w tubular neighbourhood
    spw, spu = sp.symbols("w, u", real=True) ## width of torus knot, and meridional parameter

    tSurf = c + spw*sp.cos(2*sp.pi*(spu+kp*kq*spt))*ukc + spw*sp.sin(2*sp.pi*(spu+kp*kq*spt))*bnc

    ## (b) ufuncify
    from sympy.utilities.autowrap import ufuncify
    knotSuf = [ufuncify([spt, spp, spq, spr, spR, spw, spu], tSurf[i]) for i in range(3)]
    knotSnp = sp.lambdify((spt, spp, spq, spr, spR, spw, spu), tSurf, "numpy" )

    kt = (np.pi*tr) / (4*kp) # knot radial thickness 2*pi*tr is circumf, and kp strands pass through so this
    ## should be around 2*pi*tr  would be 2*kp*kt for the knot to fill the surface, i.e kt = pi*tr / 4*kp
    ## make bigger or smaller depending on how much empty space one wants to see.

    seg = kp*refine ## segments along length of pq torus knot. kp*120 gives a fairly smooth image.

    def surf(i,j): ## lambdify
        return np.array(knotSnp(float(i)/seg, kp, kq, tr, tR, kt, float(j)/segm)).ravel()


    fp = FloatProgress(min=0, max=100, description="Knot data");     
    display(fp); ## progrss indicator

    xyz = np.ndarray( (seg+1, segm+1, 3) )
    for i,j in it.product( range(seg+1), range(segm+1) ):
        ## put the affine reparametrization here. 
        xyz[i,j] = surf(i,j)
        fp.value = int(100*i/(seg+1))
        
    fp.close()
    return(xyz)