#Problem C of ENME 337 Final Project
#Failure Probability Analysis

from random import normalvariate
import PartA
from matplotlib import pyplot as plt

##All given values from the table,these are used in the final function##  
##Do = 88.9         #pipe outer diameter, [mm]
##t =11.1252        #pipe thickness, [mm]
##a = 8.6           #fixed initial depth of crack, [mm]
##b = 14.5          #fixed initial length of crack, [mm] 
##P = 50            #Internal pipeline pressure, [MPa]
##Kic = 65          #PLane Strain Fracture Toughness, [MPam^(1/2)]
##Y                 #from probem A, geometry correction factor 
##A = 6.25e-12      #Paris Equation Coefficient, [m/cycle]
##n = 4             #Paris equation exponent
##da = 0.5          #Incremental Crack Growth, [mm]
##N = 10000         #Number of iterations, given in project outline


def user_test_run ():
    '''takes in the user's input to determine the test that is run
    -test 1, initial length of crack is fixed, initial depth of crack is a list of rand values
    -test 2, initial depth of crack is fixed, initial length of crack is a list of rand values
    -returns the value of the user input which is saved as an int
    -the function takes in the values a, b and assigns them to the corresponding fixed value depending on the test'''

    #calls for the user's input and saves it as an int
    userInput = int(input("Would you like to run Monte Carlo test 1 or 2? Test 1 keeps the initial length of the crack a fixed value while changing the initial depth of the crack and test 2 keeps the initial depth of the crack fixed while changing the initial length of the crack: "))

    with open("Results.txt","a") as results:
        results.write("Results for Problem C are \n")
        if userInput == 1:
            #this prints out the test the user is running  
            print("You have selected test 1 where the initial length of the crack is a fixed value of 14.5 mm while the initial depth of the crack is randomly sampled from the given normal distribution.")
            results.write("You have selected test 1 where the initial length of the crack is a fixed value of 14.5 mm while the initial depth of the crack is randomly sampled from the given normal distribution. \n")

        if userInput == 2:
            #this prints out the test the user is running 
            print("You have selected test 2 where the initial depth of the crack is a fixed value of 8.6 mm while the initial length of the crack is randomly sampled from the given normal distribution.")
            results.write("You have selected test 2 where the initial depth of the crack is a fixed value of 8.6 mm while the initial length of the crack is randomly sampled from the given normal distribution. \n")

        while userInput != 1 and userInput !=2:
            #if the user input is wrong, this prompts the user to enter which test they want to run again
            print("This entry is invalid, please try again inputting 1 or 2.")
            userInput = int(input("Would you like to run test 1 or 2 where test 1 keeps the initial length of the crack a fixed value while changing the initial depth of the crack and test 2 keeps the initial depth of the crack fixed while changing the initial length of the crack: "))

    return userInput        #return the user input



def get_random_value (N):
    '''-this function takes in N and creates a 10000 random value array for each of the given parameters
    -the random value array is generated for the desired lifetime of the pipeline, the initial crack depth and length
    -the random values are determined from the mean and stadard deviation for the above parameter
    -returns the array of random values for different parameters'''

    #the standard deviation and mean for the parameter which is given in the project outline
    pipe_lifetime_mean = 40*365           #days
    pipe_lifetime_stdev = 10*365          #days
    initial_crack_length_mean = 14.5/1000      #mm->m
    initial_crack_length_stdev = 1.6/1000      #mm->m
    initial_crack_depth_mean = 8.6/1000        #mm->m
    initial_crack_depth_stdev = 1.5/1000       #mm->m
    
    #creating empty array of the random values
    randval_pipe_lifetime = []
    randval_crack_length = []
    randval_crack_depth = []

    for i in range(N):
        #we append each array with a random value N times
        randval_pipe_lifetime.append(normalvariate(pipe_lifetime_mean,pipe_lifetime_stdev))
        randval_crack_length.append(normalvariate(initial_crack_length_mean,initial_crack_length_stdev))
        randval_crack_depth.append(normalvariate(initial_crack_depth_mean,initial_crack_depth_stdev))
    
    #returning a 2D array with the arrays of the random values
    return randval_pipe_lifetime, randval_crack_length, randval_crack_depth



def monte_carlo (a, b, Kic, Do, t, P, da, A, n, Lf, N, userInput):
    '''-This function takes in all the predefined values from the report
    -it then runs the code from part A to find the number of cycles to failure, Nf
    -then calculates the NumFail and calculates the probabilty of failure
    -this code prints the probability of failure and returns the list of Nf values'''

    #Based on the user's input for what test they want to run, the list of random values is created
    #the list of random values is stored as list_a

    Nf_list = []            #the list of Nf is intialized
    
    if userInput == 1:
        #test 1, initial length is fixed, initial depth is a list of rand vals
        fixed_b = b
        _,_,list_a = get_random_value(N)
        
        for i in range(N):
            #inputting the fixed values and the list of rand vals for the given test into calcA function of Problem A to find Nf
            #iterate though each value of the list of rand vals to find Nf
            #appending Nf_list with each value of Nf
            _, Ps, aav, sigmaN, Nf = PartA.calcA(float(list_a[i]), fixed_b, Kic, Do, t, P, da, A, n, Lf[i])
            Nf_list.append(Nf)
        
    if userInput == 2:
        #test 2, initial depth is fixed, initial length is a list of rand vals
        fixed_a = a
        _,list_b,_ = get_random_value(N)
    
        for i in range(N):
            #inputting the fixed values and the list of rand vals for the given test into calcA function of Problem A to find Nf
            #iterate though each value of the list of rand vals to find Nf
            #appending Nf_list with each value of Nf
            _, Ps, aav, sigmaN, Nf = PartA.calcA(fixed_a, float(list_b[i]), Kic, Do, t, P, da, A, n, Lf[i])
            Nf_list.append(Nf)

    NumFail = 0                         #initializing NumFail
    
    for j in range(N):                  #iterating through each value of Lf and Nf to find NumFail
        if Lf[j] > Nf_list[j]:
            NumFail = NumFail + 1

    Pf = NumFail/N                      #Calculation the probility of failure
    
    #printing Pf and returning Nf_list
    print("The calculated failure probabity value is:", Pf, "or", Pf*100,"%")
    with open("Results.txt","a") as results:
        results.write(f"The calculated failure probabity value is {Pf} or {Pf*100} % \n")
    
    return Nf_list


    
def plot_histogram (Nf_list, Lf):
    '''-takes in Nf_list, Lf, N and plots the histogram for the probabiltiy distribution of Nf_list and Lf'''

    #plotting the histogram of Nf_list and Lf with tite,labeled axis and semi-transparent
    plt.hist(Nf_list, alpha = 0.5, label = 'Observed Lifetime (Nf)') 
    plt.hist(Lf, alpha = 0.5, label = 'Desired Lifetime (Lf)')
    #x= [x for x in range(10000)]
    #plt.scatter(x,Nf_list)
    plt.title("Probabiltiy Distribution of the desired lifetime (Lf) of the pipe and the observed lifetime (Nf) of the pipe")
    plt.xlabel("Lifetime [Days]")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig("Plot of Probability Distributions.pdf")
    plt.show()
    

def mainC():
    '''-Function runs all the functions from above to perform a monte carlo test based on the user's input
       -outputs the test being run, the probabilty of failure, histogram of probabilty distrubution'''  
    
    #All given values from report
    Do = 88.9/1000          #pipe outer diameter,                           [mm]-->[m]
    t =11.1252/1000         #pipe thickness,                                [mm]-->[m]
    a = 8.6/1000            #fixed initial depth of crack,                  [mm]-->[m]
    b = 14.5/1000           #fixed initial length of crack,                 [mm]-->[m] 
    P = 50                  #Internal pipeline pressure,                    [MPa]
    Kic = 65                #Plane Strain Fracture Toughness,               [MPam^(1/2)]                     
    A = 6.25e-12            #Paris Equation Coefficient,                    [m/cycle]
    n = 4                   #Paris equation exponent
    da = 0.5/1000           #Incremental Crack Growth,                      [mm]-->[m]
    N = 10000

    userInput= user_test_run()                                                  #getting user input                           
    Lf, _, _ = get_random_value(N)                                              #creating the list of random values for the desired lifetime of the pipe
    Nf_list = monte_carlo(a, b, Kic, Do, t, P, da, A, n, Lf, N, userInput)      #running monte carlo test
    plot_histogram(Nf_list, Lf)                                                 #plotting the histogram

    




    
        





