




#functions for creating images of regions of the complex plane

def view_C_lin(point,Q,Window):
    C = window(point,Window)
    return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#
def inv_view_C_lin(C,Window):
    point = unwindow(C,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

# def view_C_log(point,Q,Window):
#     lnScale=math.log(abs(Window[1]-Window[0]))-0.3465735902799727
#     lnC = window(point,[complex(lnScale-math.pi,math.pi),complex(lnScale,2*math.pi)])
#     C=Window[0]+math.exp(lnC.real)*complex(math.cos(lnC.imag),math.sin(lnC.imag))
#     return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#

def view_J_lin(point,Q,Window):
    C = window(point,Window)
    if point.imag>.8 and point.real>.8 and False:
        return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
    else:
        return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#
def inv_view_J_lin(C,Window):
    point = unwindow(C,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

# def view_J_log(point,Q,Window):
#     lnScale=math.log(abs(Window[1]-Window[0]))-0.3465735902799727
#     lnC = window(point,[complex(lnScale-math.pi,math.pi),complex(lnScale,2*math.pi)])
#     C=Window[0]+math.exp(lnC.real)*complex(math.cos(lnC.imag),math.sin(lnC.imag))
#     if point.imag>.8 and point.real>.8:
#         return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
#     else:
#         return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#

#######
def complex_log(x):
    try:
        a=math.log(abs(x))
    except:
        print('log error,',x)
        a=-100
    b=math.atan2(x.imag,x.real)
    return complex(a,b)

def view_C_log_2(point,Q,Window):
    lnC = window(point,Window)
    C=windows['C_lin'][0]+exp(lnC)
    return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#
def inv_view_C_log_2(C,Window):
    lnC = complex_log(C-windows['C_lin'][0])
    point=unwindow(lnC,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

def view_J_log_2(point,Q,Window):
    lnC = window(point,Window)
    C=windows['J_lin'][0]+exp(lnC)
    #print(windows['J_lin'])
    if point.imag>.8 and point.real>.8:
        return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
    else:
        return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#
def inv_view_J_log_2(C,Window):
    lnC = complex_log(C-windows['J_lin'][0])
    point=unwindow(lnC,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

view_map=view_C_lin
inv_view_map=inv_view_C_lin











