
import math
Newton=False#change f when you change this
# In[5]:


#set up some complex functions and numbers

def inv(c):
    """Safe division, return 1/c unless c is 0, then returns 0."""
    if abs(c)==0:
        return c
    return 1/c

def rootcircle(n, initial = complex(1,0)):
    """creates a circle of n evenly spaced complex numbers starting with inital."""
    roots = [initial]
    angle = 2*math.pi/n
    rotate = complex(math.cos(angle),math.sin(angle))
    for i in range(n-1):
        roots.append(roots[-1]*rotate)
    return(roots)

#set centers to be the 3rd roots of unity
centers = rootcircle(3)

def P(C,roots = centers):
    """Creates the polynomial consisting of the product of (x-x0) for x0 in roots,
    evaluates this polynomial at the complex nubmer C"""
    p= complex(1,0)
    for root in roots:
        p = p*(C-root)
    return(p)

def dP(C,roots = centers):
    
    """Creates the derivative of the polynomial consisting of the product of (x-x0) for x0 in roots,
    evaluates this derivative at the complex nubmer C"""
    dp = complex(0,0)
    for i in range(len(roots)):
        dp = dp+(P(C,roots[:i]+roots[i+1:]))
    return(dp)
        

def P_dP(C,roots):
    """Creates the polynomial consisting of the product of (x-x0) for x0 in roots,
    returns a step calculated using newtons method (-P'(C)/P(C)). Will return 0 where P' is 0.
    """
    p_dp = -P(C,roots)*inv(dP(C,roots))
    return(p_dp)


e=complex(math.exp(1),0)
def exp(x):
    return e**x

######################################################################################################################
############################## most important function in the program right here #####################################
######################################################################################################################

def f(Z,C=0,roots=centers):#.285,.01)):#,C2 = complex(-3.0789856785439538, 0.2719380912620699)
    """the function to be iterated. Usually z^2+c, this gives the mandelbrot set. z+P_dP is newtons method."""
    global centers
    return(Z**2+C)#(Z+P_dP(Z,attractors))#or Z,roots#((Z-(Z**2))*C)#(Z**4-Z**2+C)#
#(Z**3+Z**2+C)#
#(e**Z+C)#
#    k=3/2*(2+C1+C2);#(Z**3/(6*k)+k*Z/2+(C1+C2)/2)
#((Z**2/(np.sqrt(Z.real**2+Z.imag**2)))*1.1+C)


C= complex(-0.11712655777245454, 0.6495111247984681)+complex(.080,.12)#weird spot under 3 bulb
Z=complex(0,0)
# #calculate attractors using C
# for i in range(5000):
#     Z=f(Z,C)
#     if abs(Z)>5:
#         break#commented out for newton stuff,but I don't think I need it anyway...
if abs(Z)<=5 and not Newton:#:#and False added for newton stuff#
    attractors=[Z]#+complex(.01,0)]
else:
    attractors=[complex(1),complex(-1),0]##for newton, insert at indices 0,1



def Attractor(Z,C,roots,count=100):
    """
    given Z,C, and a list of roots, calculates which (if any) of the roots is nearly (within .1)
    reached after 100 iterations of f_C at Z, returns the index of the root or None.
    """
    while count>0:
        Z=f(Z,C,roots)
        count-=1
    for center in roots:
        if abs(Z-center)<.1:
            return(roots.index(center))
    return

r_escape=max([abs(x) for x in attractors]+[1])+4+(40000-4)*int(Newton)#was 4, changed for newton stuff to 40000
r_trap=.005
def attractor(Z):
    """
    given Z, uses the global variable attractors as a list of roots, calculates which (if any) 
    of the roots is nearly (within r_trap) reached after 100 iterations of f_C at Z, returns the 
    index of the root or -1 if Z escapes to infinity.
    """
    global attractors,r_escape,r_trap
    if abs(Z)>r_escape:
        return -1
    for i,center in enumerate(attractors):
        if abs(Z-center)<r_trap:
            return(i)
    return


def set_attractors(C,maxmag=5000,newton=False):
    """Finds Z after maxmag iterations of f_C, if |Z|<5, assumes that Z is an attractor and 
    adds it to the global variable attractors"""
    global attractors
    if newton:
        attractors=[complex(1)-C/2,complex(-1)-C/2,C]
        return
    Z=complex(0,0)
    for i in range(maxmag):
        Z=f(Z,C)
        if abs(Z)>5:
            return
    attractors=[Z]#+complex(.01,0)]#[]#
set_attractors(C,15,newton=True)
def set_function_Magnitude(find_attractor=False):
    """creates and returns one of two functions, depending on find_attractor"""
    if find_attractor==True:
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            #C = Z
            #Z=complex(0,0)
            count = 0
            set_attractors(C,15)
            while count<maxcount and attractor(Z)==None:
                Z=f(Z,C)
                count+=1
            if count == maxcount: return [-1,1]
            return([count,attractor(Z)])
        return Magnitude
    elif find_attractor=='J only':
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            #C = Z
            #Z=complex(0,0)
            count = 0
            #set_attractors(C,1500)
            if Newton:
                set_attractors(C,15,newton=True)#for newton only!
            while count<maxcount and attractor(Z)==None:
                Z=f(Z,C)
                count+=1
            if count == maxcount: 
                return [-1,-1]
            return([count,attractor(Z)])
        return Magnitude
    elif find_attractor=='test_fill':
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            return [0,472]
            # #C = Z
            # #Z=complex(0,0)
            # count = 0
            # #set_attractors(C,1500)
            # if Newton:
            #     set_attractors(C,15,newton=True)#for newton only!
            # while count<maxcount and attractor(Z)==None:
            #     Z=f(Z,C)
            #     count+=1
            # if count == maxcount: 
            #     return [-1,-1]
            # return([count,attractor(Z)])
        return Magnitude
    else:
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            #C = Z
            #Z=complex(0,0)
            count = 0
            #set_attractors(C,1500)
            while count<maxcount and abs(Z)<10:
                try:
                    Z=f(Z,C)
                except:
                    break
                count+=1
            if count == maxcount: return [-1,-1]
            else: return [count,-1]
        return Magnitude