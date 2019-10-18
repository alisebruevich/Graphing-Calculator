#newest, latest, freshest
#fix derivatives with masking and unmasking arrays for x and y: Bonnie
#presentation (what we did, learned; 3-5 slides): Alise
#code block diagram: Bonnie
#test to see if exponential functions will work: Alise -> IT DOESN'T CRY
#make labels for what different colors/symbols mean on the graph: Alise -> DONE
#double check that log stuff works: Alise -> IT DOESN'T CRY

##
#f is original, g is first derivative, h is second derivative
import math as m
from tkinter import *
from sympy import *
def graph(input,a,b):
    import numpy.ma as M
    import numpy as np
    from numpy import linspace
    from sympy.parsing.sympy_parser import parse_expr
    import matplotlib.pyplot as mpl
    from sympy.parsing.sympy_parser import standard_transformations,\
    implicit_multiplication_application
    transformations = (standard_transformations +(implicit_multiplication_application,))
    mpl.axhline(color="black")
    mpl.axvline(color="black")
    x = symbols('x')
    listofx=[]
    x_vals = np.arange(-50,50,0.01)
    for i in range(0, len(x_vals)):
        x_vals[i] = round(x_vals[i],4)
    specialx_vals=x_vals
    f=parse_expr(input, transformations=transformations)#parsing function
    fy_vals=[]

    zoo = parse_expr("1/0", transformations = transformations)
    nan = parse_expr("0/0", transformations = transformations)
    for i in x_vals:
        fy_vals.append(f.subs(x,i))

    for i in specialx_vals:
        if f.subs(x,i).is_real==False:
            x_vals=x_vals[1:len(x_vals)]
            fy_vals=fy_vals[1:len(fy_vals)]
    specialx_vals=x_vals
    maskedy_vals=fy_vals

    vals=[]
    for i in range(0, len(fy_vals)):
        #Case 1: 1/0 , or zoo, which is an Asymptote
        if (fy_vals[i] == zoo):
            vals.append(x_vals[i])
        #Case 2: 0/0, or nan, which is a Hole
        elif (fy_vals[i] == nan):
            vals.append(x_vals[i])

    #graph derivative
    gy_vals=differentiate(x_vals,fy_vals)
    maskedgy_vals=gy_vals
    x_vals=x_vals[0:len(x_vals)-1]
    for i in range(0, len(vals)):
        maskedgy_vals = M.masked_where(x_vals == vals[i], maskedgy_vals)
    maskedgy_vals = M.masked_where(x_vals == x_vals[0], maskedgy_vals)
    mpl.plot(x_vals, maskedgy_vals,color="orange")#orange
    if isnumeric(a) and isnumeric(b):
        a=float(a)
        b=float(b)
        integrate(f,a,b)

    #graph 2nd derivative
    hy_vals=differentiate(x_vals,gy_vals)
    maskedhy_vals=hy_vals
    x_vals=x_vals[0:len(x_vals)-1]
    for i in range(0, len(vals)):
        maskedhy_vals = M.masked_where(x_vals == vals[i], maskedhy_vals)
    maskedhy_vals= M.masked_where(x_vals==x_vals[0],maskedhy_vals)
    maskedhy_vals= M.masked_where(x_vals==x_vals[1],maskedhy_vals)
    mpl.plot(x_vals, maskedhy_vals, color="green")#green

    #graph discontinuities
    lastFunction = simplify(f)
    print(lastFunction)

    for i in range(0, len(fy_vals)):
        #Case 1: 1/0 , or zoo, which is an Asymptote
        if (fy_vals[i] == zoo):
            print("it's asymptote!")
            maskedy_vals = M.masked_where(specialx_vals == specialx_vals[i], maskedy_vals)
            mpl.axvline(x=specialx_vals[i], color='r')
        #Case 2: 0/0, or nan, which is a Hole
        elif (fy_vals[i] == nan):
            print("it's a hole!")
            maskedy_vals = M.masked_where(specialx_vals == specialx_vals[i], maskedy_vals)
            mpl.plot(specialx_vals[i],lastFunction.subs(x, specialx_vals[i]),color="black",marker="p")
    mpl.plot(specialx_vals, maskedy_vals,color="blue")#plots#blue

    #find extrema
    #extrema are graphed as pink pentagons
    basically_zero = 1*10**-4
    #print(x_vals)
    for i in range(0,len(gy_vals)-1):
        if (not(gy_vals[i]== nan or gy_vals[i]==zoo)) and abs(gy_vals[i])<basically_zero:
            if gy_vals[i-1]>basically_zero and gy_vals[i+1]<(basically_zero*-1):
                mpl.plot(x_vals[i],maskedy_vals[i],color="#FF00FC",marker="p")
                print("extrema:")
                print(x_vals[i])
                print(maskedy_vals[i])
            if gy_vals[i-1]<(-1*basically_zero) and gy_vals[i+1]>basically_zero:
                mpl.plot(x_vals[i],maskedy_vals[i],color="#FF00FC",marker="p")
                print("extrema:")
                print(x_vals[i])
                print(maskedy_vals[i])
        elif (not(gy_vals[i]== nan or gy_vals[i]==zoo)) and (not(gy_vals[i+1]== nan or gy_vals[i+1]==zoo)) and gy_vals[i]>0 and gy_vals[i+1]<0:
            xbetween=np.arange(x_vals[i],x_vals[i+1],0.00001)
            betweenvals=[]
            fbetween=[]
            for i in xbetween:
                fbetween.append(f.subs(x,i))
            maskedfbetween=fbetween
            for i in range(0,len(maskedfbetween)):
                if maskedfbetween[i] == zoo or maskedfbetween == nan:
                    betweenvals.append(xbetween[i])
            for i in range(0, len(betweenvals)):
                maskedfbetween = M.masked_where(xbetween == betweenvals[i], maskedfbetween)
            gbetween=differentiate(xbetween,fbetween)
            for i in range(0,len(gbetween)-1):
                if abs(gbetween[i])<basically_zero:
                    if gbetween[i-1]>0 and gbetween[i+1]<0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="p")
                        print("extrema:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
                    if gbetween[i-1]<0 and gbetween[i+1]>0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="p")
                        print("extrema:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
        elif (not(gy_vals[i]== nan or gy_vals[i]==zoo))  and (not(gy_vals[i+1]== nan or gy_vals[i+1]==zoo)) and gy_vals[i]<0 and gy_vals[i+1]>0:
            xbetween=np.arange(x_vals[i],x_vals[i+1],0.00001)
            betweenvals=[]
            fbetween=[]
            for i in xbetween:
                fbetween.append(f.subs(x,i))
            maskedfbetween=fbetween
            for i in range(0,len(maskedfbetween)):
                if maskedfbetween[i] == zoo or maskedfbetween == nan:
                    betweenvals.append(xbetween[i])
            for i in range(0, len(betweenvals)):
                maskedfbetween = M.masked_where(xbetween == betweenvals[i], maskedfbetween)
            gbetween=differentiate(xbetween,fbetween)
            for i in range(0,len(gbetween)-1):
                if abs(gbetween[i])<basically_zero:
                    if gbetween[i-1]>0 and gbetween[i+1]<0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="p")
                        print("extrema:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
                    if gbetween[i-1]<0 and gbetween[i+1]>0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="p")
                        print("extrema:")
                        print(xbetween[i])
                        print(maskedfbetween[i])

    #find inflection points
    #inflection points are graphed as green stars
    for i in range(0,len(hy_vals)-1):
        if (not(hy_vals[i]== nan or hy_vals[i]==zoo)) and abs(hy_vals[i])<basically_zero:
            if not(hy_vals[i-1]== nan or hy_vals[i+1]==zoo):
                if hy_vals[i-1]>basically_zero and hy_vals[i+1]<(basically_zero*-1):
                    mpl.plot(x_vals[i],maskedy_vals[i],color="#FF00FC",marker="*")
                    print("inflection:")
                    print(x_vals[i])
                    print(maskedy_vals[i])
                if hy_vals[i-1]<(-1*basically_zero) and hy_vals[i+1]>basically_zero:
                    mpl.plot(x_vals[i],maskedy_vals[i],color="#FF00FC",marker="*")
                    print("inflection:")
                    print(x_vals[i])
                    print(maskedy_vals[i])
        elif (not(hy_vals[i]== nan or hy_vals[i]==zoo)) and (not(hy_vals[i+1]== nan or hy_vals[i+1]==zoo)) and hy_vals[i]>0 and hy_vals[i+1]<0:
            xbetween=np.arange(x_vals[i],x_vals[i+1],0.00001)
            betweenvals=[]
            fbetween=[]
            for i in xbetween:
                fbetween.append(f.subs(x,i))
            maskedfbetween=fbetween
            for i in range(0,len(maskedfbetween)):
                if maskedfbetween[i] == zoo or maskedfbetween == nan:
                    betweenvals.append(xbetween[i])
            gbetween=differentiate(xbetween,fbetween)
            xbetween=xbetween[0:len(xbetween)-1]
            maskedgbetween=gbetween
            for i in range(0, len(betweenvals)):
                maskedgbetween = M.masked_where(xbetween == betweenvals[i], maskedgbetween)
            hbetween=differentiate(xbetween,gbetween)

            for i in range(0,len(hbetween)-1):
                if abs(hbetween[i])<basically_zero:
                    if hbetween[i-1]>0 and hbetween[i+1]<0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="*")
                        print("inflection:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
                    if hbetween[i-1]<0 and hbetween[i+1]>0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="*")
                        print("inflection:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
        elif (not(hy_vals[i]== nan or hy_vals[i]==zoo)) and (not(hy_vals[i+1]== nan or hy_vals[i+1]==zoo)) and hy_vals[i]<0 and hy_vals[i+1]>0:
            xbetween=np.arange(x_vals[i],x_vals[i+1],0.00001)
            betweenvals=[]
            fbetween=[]
            for i in xbetween:
                fbetween.append(f.subs(x,i))
            maskedfbetween=fbetween
            for i in range(0,len(maskedfbetween)):
                if maskedfbetween[i] == zoo or maskedfbetween == nan:
                    betweenvals.append(xbetween[i])
            gbetween=differentiate(xbetween,fbetween)
            xbetween=xbetween[0:len(xbetween)-1]
            maskedgbetween=gbetween
            for i in range(0, len(betweenvals)):
                maskedgbetween = M.masked_where(xbetween == betweenvals[i], maskedgbetween)
            hbetween=differentiate(xbetween,gbetween)
            for i in range(0,len(hbetween)-1):
                if abs(hbetween[i])<basically_zero:
                    if hbetween[i-1]>0 and hbetween[i+1]<0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="*")
                        print("inflection:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
                    if hbetween[i-1]<0 and hbetween[i+1]>0:
                        mpl.plot(xbetween[i],maskedfbetween[i],color="#FF00FC",marker="*")
                        print("inflection:")
                        print(xbetween[i])
                        print(maskedfbetween[i])
    mpl.axhline(color="black")
    mpl.axvline(color="black")
    mpl.xlim(-5,5)
    mpl.ylim(-10, 10)
    mpl.grid(b=True)#sets grid
    mpl.show()

def isnumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def differentiate(x,y): #takes in arguments: list of x values and list of y values
    gy_vals=[] #makes list of derivative values
    for n in range(1,len(x)-1): #loops through x values
        hi=(y[n+1]-y[n-1])/(x[n+1]-x[n-1]) #finds the slope using the values around it
        gy_vals.append(hi) #adds it to the list
    gy_vals.insert(0,gy_vals[0])
    return gy_vals #returns derivative values

##############integrate function
def integrate(f,a,b): #takes in arguments: function f, lower bound a, and upper bound b
    import numpy.ma as M
    import numpy as np
    from numpy import linspace
    from sympy.parsing.sympy_parser import parse_expr
    import matplotlib.pyplot as mpl

    x = symbols('x')
    #generates list of x values in small increments in between a and b
    if a<b:
        xvals=np.arange(a,b,0.001)
    if a>b:
        xvals=np.arange(b,a,0.001)
    if a==b:
        return
    fyvals=[]
    for i in xvals:
        fyvals.append(f.subs(x,i)) #creates list of y vals that correspont to x vals
    gyvals=differentiate(xvals,fyvals) #gets list of derivative values
    xvals=xvals[0:len(xvals)-1]
    sum=0
    for n in range(0,len(xvals)-1): #finds areas of trapezoids and then adds them to sum
        trapezoid=0.5*(xvals[n+1]-xvals[n])*(gyvals[n]+gyvals[n+1])
        sum+=trapezoid
    ftc=f.subs(x,b)-f.subs(x,a) #calculates f(b)-f(b) which should be equal to the sum
    thing="%s = %s" %(sum,ftc) #puts the equality on the graph
    mpl.text(0,0,thing)
def evaluate(event):
    input= entry1.get()
    a=entrya.get()
    b=entryb.get()
    graph(input,a,b)
w = Tk()
w.title("Graphing Calculator")
Label(w, text="Your Expression:").pack()
entry1 = Entry(w)
entry1.bind("<Return>", evaluate)
entry1.pack()
Label(w, text="a:").pack()
entrya = Entry(w)
entrya.bind("<Return>", evaluate)
entrya.pack()
Label(w, text="b:").pack()
entryb = Entry(w)
entryb.bind("<Return>", evaluate)
entryb.pack()
Label(w, text="MARKERS:").pack()
Label(w, text="Extrema are graphed as pink pentagons").pack()
Label(w, text="Inflection points are graphed as pink stars").pack()
Label(w, text="Asymptotes graphed as a red line").pack()
Label(w, text="Holes graphed as black pentagons").pack()
res = Label(w)
res.pack()
w.mainloop()
