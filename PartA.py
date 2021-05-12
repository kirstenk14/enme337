###Problem A (Parts 1-4)###

#Database: Pipe outer diameter (Do),
#          Pipe wall thickness (t),
#          Plane strain fracture toughness factor (Kic),
#          Paris equation coefficient (A),
#          Paris equation exponent (n)
#User input: Initial crack depth (a),
#            Initial crack length (b),
#            Internal pipeline pressure (P),
#            Desired Lifetime of the pipe (Lf),
#            Incremental crack growth (da)
#To be calculated: Pipe inner diameter (Di),
#                  Geometry correction factor (Y),
#                  L,
#                  Surge pressure (Ps),
#                  Hoop stress (Sh),
#                  Total stress (St),
#                  Critical crack depth (acr),
#                  Lifetime of the pipe (Nf),
#                  List containing number of cycles per iteration of the loop in calcA (dN),
#                  List containing starting a value for each iteration of the loop (a_o),
#                  List containing final a value for each iteration (a_f),
#                  List containing average of a_o and a_f values for each iteration (aav),
#                  List containing sum of cycles (sum of dN) for every iteration up to that one (sigmaN),
#                  List containing K values for each iteration (K)



import csv
import math
import numpy as np
import matplotlib.pyplot as plt

def convInches(val_inches):
    val_meters = val_inches/(39.37)
    return val_meters
def convMilimeters(val_mm):
    val_meters = val_mm/(1000)
    return val_meters
def convYears(val_yrs):
    val_days = val_yrs*365
    return val_days

###PART 1###
#User Input and Exception Handling 
#Keep the User Input for NPS as a String so that it can be found in the PipeData.csv File
def userInput():
    NPS = input("Enter a Nominal Pipe Size as an Integer or Float (inches)")    
    pipe_sched = input("Enter a Pipe Schedule (No Units)")
    pipe_mat = input("Enter a Pipe Material (No Units)")

    #Look up Values in CSV
    #Check if File is Closed, if File cannot be Read or cannot be Opened
    #Check if Wall Thickness varies from Standard Values (Print a Warning Message if Applicable)
    #This is if Wall Thickness from User Input is less than or greater than the Standard Values for Wall Thickness 

    #Path is assigned to a variable so it can be changed when code is run on a different computer
    #Keyword "with" is used so file is automatically closed
    pipe_file = "/Users/Kirsten Korsrud/Downloads/PipeData.csv"
    try:
        with open(pipe_file, 'r') as pipe_data:
            try:
                pipe_read = csv.reader(pipe_data)
                next(pipe_read) #Skip Header Row next() from https://stackoverflow.com/questions/35329573/finding-max-value-in-a-column-of-csv-file-python
                for row in pipe_read:
                    if (row[0] == NPS) and (row[2] == pipe_sched):
                        D_o = float(row[1]) #Actual Outer Diameter (inches)
                        t = float(row[3]) #Wall Thickness (inches)
                    elif (row[0] == NPS) and (row[2] == '-' or row[2] == '--'):
                        D_o = float(row[1])
                        t = float(input("Enter the Wall Thickness of the Pipe as an Integer or Float greater than 0 in inches."))
                        while t == 0:
                            t = float(input("Enter the Wall Thickness of the Pipe as an Integer or Float in inches. Entered value was equal to 0 which will cause a DivisionByZero Error"))
                        if t < 0.049 or t > 2.344: #Minimum and Maximum t values calculated with excel functions
                            print("WARNING! Entered Wall Thickness of the Pipe in inches varies from Standard Values.")
                            break
                        else:
                            break
            except IOError as e:
                print(e) #Trying to Read a Closed File 
            except:
                print("Error in Reading File") 
    except:
        print("Error in Opening the File")
    #Convert Units (inches to meters) for NPS, D_o, t
    #Typecast NPS from String to Float for Future Calculations if Needed
    NPS = convInches(float(NPS))
    D_o = convInches(D_o)
    t = convInches(t)
  
    mat_file = "/Users/Kirsten Korsrud/Downloads/MaterialData.csv"
    try:
        with open(mat_file, 'r') as mat_data:
            try:
                mat_read = csv.reader(mat_data)
                next(mat_read) #Skip Header Row
                for row in mat_read:
                    if row[0] == pipe_mat and row[2] != '-':
                        KIC_min = float(row[2]) 
                        KIC_max = float(row[3])
                        K = (KIC_min + KIC_max)/2 #Plane Strain Fracture Toughness (MPa m^1/2)
                        A = float(row[4]) #Paris Equation Coefficient (meters/cycle)
                        n = float(row[5]) #Paris Equation Exponent (No Units)
                        break
                    elif row[0] == pipe_mat and row[2] == '-':
                        K = float(row[3])
                        A = float(row[4])
                        n = float(row[5])
                        break
            except IOError as e:
                print(e) #Trying to Read a Closed File
            except:
                print("Error in Reading File")
    except:
        print("Error in Opening the File")

    
    ###PART 2###

    #User Input and Exception Handling
    #Check if the Entered values are Integers or Floats and Within a Given Range if Applicable
    try:
        a = float(input("Enter Initial Depth of the Crack as an Integer or Float(in mm)"))
    except:
        a = float(input("Enter Initial Depth of Crack as an Integer or Float(in mm) Again. Entered Value was not an Integer or Float."))
    try:
        b = float(input("Enter the Length of the Crack as an Integer or Float greater than 0 (in mm)."))
    except:
        b = float(input("Enter Length of Crack as an Integer or Float(in mm) Again. Entered Value was not an Integer or Float."))
    while b == 0:
        b = float(input("Enter the Length of the Crack as an Integer or Float (in meters) again. Entered Value was equal to 0 and will cause a DivisionbyZero Error."))
    try:
        P = float(input("Enter the Internal Pressure in MPa from 40-2000MPa"))
    except:
        P = float(input("Enter the Internal Pressure in MPa from 40-2000MPa Again. Entered Value was not an Integer or Float."))
    while P < 40 or P > 2000:
        P = float(input("Enter the Internal Pressure in MPa from 40-2000MPa Again. Entered Value was Below 40MPa or Above 2000MPa."))
    try:
        Lf = float(input("Enter the Desired Lifetime of the Pipeline in years from 10-50 years"))
    except:
        Lf = float(input("Enter the Desired Lifetime of the Pipeline in years from 10-50 years Again. Entered Value was not an Integer or Float."))
    while Lf < 10 or Lf > 50:
        Lf = float(input("Enter the Desired Lifetime of the Pipeline in years from 10-50 years Again. Entered Value was Below 10 years or Above 50 years."))
    try:
        da = float(input("Enter the Incremental Crack Growth in milimeters from 0.5-1.0 mm"))
    except:
        da = float(input("Enter the Incremental Crack Growth in milimeters from 0.5-1.0 mm again. Entered Value was not an Integer or Float."))    
    while da < 0.5 or da > 1.0:
        da = float(input("Enter the Incremental Crack Growth in milimeters from 0.5-1.0 mm again. Entered Value was Below 0.5mm or Above 1.0mm"))
    #Convert da from mm to meters 
    da = convMilimeters(da)
    a = convMilimeters(a)
    b = convMilimeters(b)
    Lf = convYears(Lf)
    #List of User Inputs
    user_inputs = [["Nominal Pipe Size in Meters", NPS],
                   ["Pipe Schedule", pipe_sched],
                   ["Pipe Material", pipe_mat],
                   ["Initial Depth of the Crack in Meters", a],
                   ["Length of the Crack in Meters",b],
                   ["Internal Pressure in MPa",P],
                   ["Desired Lifetime of the Pipeline in Days", Lf],
                   ["Incremental Crack Growth in Meters", da]]
    print("User Inputs are:", user_inputs)
    with open("Results.txt","a") as results: 
        results.write("Results for Problem A \n")
        results.write("User inputs are \n")
        results.write(f"Nominal Pipe Size in Meters is {NPS} \n")
        results.write(f"Pipe Schedule is {pipe_sched} \n")
        results.write(f"Pipe Material is {pipe_mat} \n")
        results.write(f"Initial Depth of the Crack in Meters is {a} \n")
        results.write(f"Length of the Crack in Meters is {b} \n")
        results.write(f"Internal Pressure in MPa is {P} \n")
        results.write(f"Desired Lifetime of the Pipeline in Days is {Lf} \n")
        results.write(f"Incremental Crack Growth in Meters is {da} \n")
    return a,b,K,D_o,t,P,da,A,n,Lf
    
def Ycalc(a,b,t):
    ###PART 4###

    #Calculate the Geometry Correction Factor (Y)
    #Note "a" from PART 2 is used
    #Create a List of Desired a/c values
    #Find the Smallest Absolute Difference between user input a/c value and desired a/c values
    #The index corresponding to the smallest absolute difference will be the a/c value that is used
    c = b/2
    ac_calc = a/c 
    ac_list = [1.00,0.80,0.40,0.20,0.10,0.02]
    ac_diff = [abs(x-ac_calc) for x in ac_list] #List Comprehension Logic from https://stackoverflow.com/questions/4918425/subtract-a-value-from-every-number-in-a-list-in-python
    ac_index = ac_diff.index(min(ac_diff)) #Finding Index from List Element from https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
    a_div_c = ac_list[ac_index]

    #Check if File is Closed, if File cannot be Read or cannot be Opened
    #Skip Blank Rows in CSV File using a counter and a conditional statement 
    #The length of a column is the number of entries or rows in that column. Therefore since indices in Python start at 0 we subtract 1 and we also subtract 1 since we do not want to use the Header row.
    #Therefore the length of a column is subtracted by 2
    x_vals = list()
    y_vals = list()
    counter = 0
    ygraph_file = "/Users/Kirsten Korsrud/Downloads/YGraphData.csv"
    try:
        with open(ygraph_file, 'r') as ygraph_data:
            try:
                ygraph_read = csv.reader(ygraph_data)
                next(ygraph_read) #Skip Header Row
                for row in ygraph_read:
                    if (a_div_c == 1.00):
                        x_vals.append(float(row[10]))
                        y_vals.append(float(row[11]))
                        counter += 1
                        if counter == (len(row[10])-2):
                            break
                    elif (a_div_c == 0.80):
                        x_vals.append(float(row[8]))
                        y_vals.append(float(row[9]))
                        counter += 1
                        if counter == (len(row[8])-2):
                            break
                    elif (a_div_c == 0.40):
                        x_vals.append(float(row[6]))
                        y_vals.append(float(row[7]))
                        counter += 1
                        if counter == (len(row[6])-2):
                            break
                    elif (a_div_c == 0.20):
                        x_vals.append(float(row[4]))
                        y_vals.append(float(row[5]))
                        counter += 1
                        if counter == (len(row[4])-2):
                            break
                    elif (a_div_c == 0.10):
                        x_vals.append(float(row[2]))
                        y_vals.append(float(row[3]))
                        counter += 1
                        if counter == (len(row[2])-2):
                            break
                    elif (a_div_c == 0.02):
                        x_vals.append(float(row[0]))
                        y_vals.append(float(row[1]))
                        counter += 1
                        if counter == (len(row[0])-2):
                            break
                    else:
                        print("Cannot Obtain Geometry Correction Factor(Y)")
                        break
            except IOError as e:
                print(e) #Trying to Read a Closed File 
            except:
                print("Error in Reading File")
    except:
        print("Error in Opening the File")

    #Polyfit uses the x_vals, y_vals and degree to get the coefficients for the equation in descending powers of x
    #PolyID uses those coefficients from Polyfit to get the equation of degree specified 
    #The Geometry Correction Factor (GCF) is calculated using a/t as the x value to sub into the equation to find y
    #https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
    #https://numpy.org/doc/stable/reference/generated/numpy.poly1d.html
    #http://scipy-lectures.org/intro/numpy/auto_examples/plot_polyfit.html
    a_div_t = a/t
    if (a_div_c == 1.00):
        poly_1 = np.poly1d(np.polyfit(x_vals,y_vals,1))
        GCF = poly_1(a_div_t)
    elif (a_div_c == 0.40):
        poly_3 = np.poly1d(np.polyfit(x_vals,y_vals,3))
        GCF = poly_3(a_div_t)
    elif (a_div_c == 0.80) or (a_div_c == 0.20) or (a_div_c == 0.10) or (a_div_c == 0.02):
        poly_4 = np.poly1d(np.polyfit(x_vals,y_vals,4))
        GCF = poly_4(a_div_t)
    return GCF


###PART 3,5-9###
def calcA(a, b, Kic, Do, t, P, da, A, n, Lf):
    Y = Ycalc(a,b,t) #No Units
    
    Di = Do - 2*t #Pipe inner diameter = Outer diameter - 2*wall thickness
    L = Do/Di #Variable L = Do/Di
    if (Do/2*t) > 20: #thin wall
        Ps = Kic/(Y*(Do/2*t)*math.sqrt(a*math.pi))
        Sh = P*(Di/2*t)
    else: #thick wall
        Ps = Kic/(Y*((2*(L**2))/((L**2)-1))*math.sqrt(a*math.pi))
        Sh = P*(((L**2)+1)/((L**2)-1))
    St = Sh+P
    acr = ((Kic/(Y*St))**2)/math.pi
    if acr > t:
        acr = t
    
    #Initializing empty matrices for a_o, a_f, aav, K, dn and sigmaN
    a_o = []
    a_f = []
    aav = []
    K = []
    dN = []
    sigmaN = []
    i = a                              #assigning counter variable for while loop

    while i > acr or i < acr:          # while loop appends array values in order to create table that shows each iteration  
        if a > acr:                    # For the case that initial depth (a) is greater than critical crack depth (acr)
            a_o.append(acr)            # the value of acr is appended to a_o, a_f, aav. sigmaN, dN, and therefore Nf are zero. (Pipe is already fractured)    
            a_f.append(acr)
            aav.append(acr)
            Kval = Y*St*math.sqrt((acr)*math.pi)  
            K.append(Kval)
            dN.append(0)
            sigmaN.append(0)
            break
            
        elif i+da > acr:              # if crack depth (a) is less than acr, but a + da is greater than acr, da is instead changed to the difference between acr and a,
            da = acr-i                # so that the final a_f value equals acr and does not exceed it.
            a_o.append(i)
            a_f.append(i+da)
            aav.append((i+i+da)/2)
            Kval = Y*St*math.sqrt(((i+i+da)/2)*math.pi)
            K.append(Kval)
            dN.append(da/(A*(Kval**n)))
            sigmaN.append(sum(dN))

        else:
            a_o.append(i)             # this loop starts off with the initial crack depth (a) and increments by da for each loop, up until a + da > acr.
            a_f.append(i+da)          # At that point, the loop above is executed instead.
            aav.append((i+i+da)/2)
            Kval = Y*St*math.sqrt(((i+i+da)/2)*math.pi)
            K.append(Kval)
            dN.append(da/(A*(Kval**n)))
            sigmaN.append(sum(dN))
            i = i+da
    
    Nf = round((sigmaN[-1]/50)*50)
    
    return Lf, Ps, aav, sigmaN, Nf

def print_outputs(Lf, Ps, Nf):
    print("The Surge Pressure that can cause Fracture is: " , Ps)
    print("Number of Cycles to Failure (Nf) is: " , Nf)

    with open("Results.txt","a") as results:
        results.write(f"The Surge Pressure that can cause Fracture is {Ps} \n")
        results.write(f"Number of Cycles to Failure (Nf) is {Nf} \n")
        
        if Nf > Lf:
            print("The Fatigue Life is greater than the Desired Lifetime of the Pipe.")
            print("The Pipe will Fail after the Desired Lifetime is reached.")
            results.write("The Fatigue Life is greater than the Desired Lifetime of the Pipe. \n")
            results.write("The Pipe will Fail after the Desired Lifetime is reached. \n")
        else:
            print("The Fatigue Life is not greater than the Desired Lifetime of the Pipe.")
            results.write("The Fatigue Life is not greater than the Desired Lifetime of the Pipe. \n")
    
        


def graphA(sigmaN, aav):

    fig, ax = plt.subplots(1,1)
    ax.scatter(sigmaN , aav ,c='blue')
    ax.plot(sigmaN, aav, c='blue')
    
    
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_ylabel("Average Crack Depth (m)")
    ax.set_xlabel("Total Cycles to Failure (Nf)")
    ax.set_title("Plot of Crack Depth vs. Total Cycles to Failure")
    ax.grid(which = 'both', color = 'red', linestyle = '--', linewidth = 0.7)
    plt.savefig("Plot of crack depth (aav) vs total cycles to failure on a log-log scale.pdf")

    return ax

def mainA():
    a,b,K,D_o,t,P,da,A,n,Lf = userInput()
    Lf, Ps, aav, sigmaN, Nf = calcA(a,b,K,D_o,t,P,da,A,n,Lf)
    print_outputs(Lf, Ps, Nf)
    graphA(sigmaN, aav)

    plt.show()
    

#mainA()
    




