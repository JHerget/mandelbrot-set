# In[4]:

import math
import numpy as np
# set up the color system for the images
def brightness(x):
    """takes 0<=x<=6, returns a two-digit hex number based on the pattern
          1****2****3
         *           *
        *             *
       *               *
      *                 *
     0                   4****5****6
    """
    if 0<x<1:
        num=int(255*x)
    elif 1<=x<=3:
        return('ff')
    elif 3<x<4:
        num=int(255*(4-x))
    else:
        return('00')
    num = hex(num)[2:]
    #print(num)
    return('0'*(2-len(num))+num)

def num_to_color(rgb):
    """Converts an rgb tuple to a hex color"""
    color='#'
    for c in rgb:
        c = hex(c)[2:]
        c='0'*(2-len(c))+c
        color=color+c
    return color
    

phi=(math.sqrt(5)+1)/2
def attractor_color(x):
    """x is an integer or None. Returns a uniqe color, black if None"""
    global phi
    if x==None:
        return('#000000')
    return(markColor(1+phi*x))

def markColor(x,brightness=brightness):
    """Takes x and a function. Uses the function on r,g,b to create a cycle of hex colors, x%6 picks a color"""
    #if x==0:
    #    return('#000000')
    cycle=x%6
    red=brightness((cycle+2)%6)
    green=brightness(cycle)
    blue=brightness((cycle-2))
    hue='#'+red+green+blue
    return(hue)

def color_ring(color0,bx,by,n):
    """given 3 vectors (lists) in R^3 and integer n, creates the hex color cycle of n colors: color0 + bx*cos(t) + by*sin(t), 0<=t<2*pi,
    replacing any colors that give errors with a different color."""
    l=[]
    t=0
    dt=2*math.pi/n
    for i in range(n):
        new=[color0[i]+ math.cos(t)*bx[i]+math.sin(t)*by[i] for i in range(3)]
        l.append(list(new))
        t=t+dt
    for i in range(len(l)):
        for j in range(3):
            l[i][j]=int(max(0,min(255,l[i][j])))
    result=[num_to_color(color) for color in l]
    return result
def color_ball(color0,bx,by,bz,n,k):
    """given 4 vectors (lists) in R^3 and integers n,k, creates the hex color cycle of n colors consisting of k rings whose
    axes revolve around bz.
    replacing any colors that give errors with a different color."""
    breakup=[n//k+int(i<n%k) for i in range(k)]
    if sum(breakup)!=n:
        for i in range(100):
            print('color ball function is faulty')
        return
    result=[]
    t=0
    dt=2*math.pi/k
    for n_i in breakup:
        b_new=[math.cos(t)*bx[i]+math.sin(t)*by[i] for i in range(3)for i in range(3)]
        result.extend(color_ring(color0,bz,b_new,n_i))
        t+=dt

        
    return result
        
def highbrightness(n):
    """creates a list of n hex colors in a cycle, bright eastery theme."""
    l=[]
    for i in range(n):
        x=(3*i/n+1/2)%3
        r=int(((-abs(x-1)+2*abs(x-2)-1+x)/2)*255)
        g=int((-(abs(x-1)+abs(x-2)-3)/2)*255)
        b=int(((-abs(2-x)+2*abs(1-x)+2-x)/2)*255)
        l.append(num_to_color((r,g,b)))
    return l
def lowbrightness(n):
    """creates a list of n hex colors in a cycle, bright eastery theme."""
    l=[]
    for i in range(n):
        x=(3*i/n+1/2+3/2)%3
        r=255-int(((-abs(x-1)+2*abs(x-2)-1+x)/2)*255)
        g=255-int((-(abs(x-1)+abs(x-2)-3)/2)*255)
        b=255-int(((-abs(2-x)+2*abs(1-x)+2-x)/2)*255)
        l.append(num_to_color((r,g,b)))
    return l
def standard_colors(n):
    return [markColor(i*6/n) for i in range(n)]
#print(highbrightness(30))
colormap=None
def set_colormap(Newton=False):
    """creates a colormap using the attractors and the point at infinity"""
    lines=[]##insert at indices 1,2 for newton
    global colormap
    if Newton:
        colormap= [highbrightness(100),lowbrightness(100),color_ring([127,127,127],[128,-64,-64],[0,111,-111],100),standard_colors(100)]#color_ball([192,64,64],[96,-96,0],[48,48,-96],[96,96,96],300,3)]#
    else:
        colormap= [highbrightness(100),standard_colors(100)]
def get_color(mag):
    """takes a list [count,i] and chooses a color cycle corresponding to attractor 'i' and a color 
    within that cycle based on 'count'"""
    
    if mag[0]==-1:
        return '#000000'
    global colormap
    if mag[1]==-1 or len(colormap)==1:
        line=colormap[-1]
    else:
        line=colormap[mag[1]%(len(colormap)-1)]
    #print(mag,len(line),mag[0]%len(line))
    return line[int(mag[0]%len(line))]
    

    
# In[16]:

#You can use the color maps from matplotlib and apply them without any matplotlib figures etc. 
#This will make things much faster:

# import matplotlib.pyplot as plt

# # Get the color map by name:
# cm = plt.get_cmap('gist_rainbow')

# # Apply the colormap like a function to any array:
# colored_image = cm(image)

# # Obtain a 4-channel image (R,G,B,A) in float [0, 1]
# # But we want to convert to RGB in uint8 and save it:
# Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8)).save('test.png')
