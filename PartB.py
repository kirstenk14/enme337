import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

    
def mainB():
# this function, mainB(), is the main function of Part B that executes every other function and call. This function does not require any input parameters
# but is called in the Main Menu file

    W = (np.linspace(25,80,4))/1000                                     # W is a numpy array (1x4) created using linspace to cover the range of values given
    B = (np.linspace(2,20,4))/1000                                      # B is a numpy array (1x4) created using linspace to cover the range of values given

    pMax = 6.14*1000
    pMin = 0.089*1000
    filename =  "/Users/Kirsten Korsrud/Downloads/avsN.csv"
    with open("Results.txt","a") as results:                            # saving and writing the results to a Results.txt file
        print(f"The values of W are:      The values of B are:  ")
        results.write("Results for B are \n")
        results.write(f"The values of W are:      The values of B are:  \n")
        for count_WB in range(len(W)):               
            print(f"       {round(W[count_WB],2)}                   {round(B[count_WB],2)} ")
            results.write(f"       {round(W[count_WB],2)}                   {round(B[count_WB],2)} \n")
    
    try:                                                                # exception handling for file opening
        with open(filename, "r") as csvFile:
            csvRead = csv.reader(csvFile)                               # csv reader reads content of avsN.csv
            header = next(csvRead)                                      # the header and preceding space are skipped in order to begin collecting data at correct spot
            space = next(csvRead)
            
            csvList = list(csvRead)                                     # creating a list copy of the csv file
            N = []
            a = []
            
            for row in range(0,len(csvList), 2):
                N.append(int( csvList[row][0] ))                        # N values stored into a list (1x24)
                a.append(float( csvList[row][1] )/1000)                 # a values in a list (1x24)
    

        plot_aN_graph = plot_aN(a,N)                                    # plot function for crack depth (a) vs. number cycles (N) 
        
        da_dN = fatigueCrackRate(a,N)                                   # fatigue crack rate values stored in array (23 long)
        
        avg_of_a = avgCrackSize(a)                                      # calculate average value of a (crack depth)
        
        arrayOfK = []
        for i in range(len(W)):
            arrayOfK.append(calcK(avg_of_a,pMax,pMin,W[i],B[i]))        # arrayOfK is a 2D array containing K calculations. ex. row 1 contains 23 values for W[0] and B[0]

        plot_K(da_dN,arrayOfK)                                          # plot_K is the function that creates the figure containing subplots of da_dN vs. K

        plt.show()
        
    except IOError as e:
        print(e)
        print("There was an error in opening the file. Ensure correct file path and name is being used.")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------         
                   
def plot_aN(a,N):
# this function, plot_aN(), intakes lists a and N. An axes object, ax, is created in order to graph
# a vs. N in a scatter plot format. plot_aN returns the ax object

    fig, ax=plt.subplots(1,1)                            
    ax.scatter(N,a, c='r')                                             # scatter graph of Number of Cycles vs. Crack Depth
    ax.set_title("Number of Cycles N vs. Crack Depth a")
    ax.set_ylabel("Crack Depth (m)")
    ax.set_xlabel("Number of Cycles")
    plt.savefig("a vs N.pdf")                                          # figure is saved as a pdf file
    return ax
    
def fatigueCrackRate(a,N):
# this function, fatigueCrackRate(), intakes lists a and N. An empty list, da_dN is created where the values of the
# secant-method numbers (between a and N) are inputted into da_dN. This funtion returns da_dN 

    da_dN = []

    for count in range(len(a)-1):
        da_dN.append((a[count+1]-a[count])/(N[count+1]-N[count]))      # da_dN is a (1x23) list 

    return(da_dN)        

def avgCrackSize(a):
# this function, avgCrackSize(), intakes lists a and calculates the average value between adjacent 2 adjacent values.
# avg_of_a is returned

    avg_of_a = []
    for count in range(len(a)-1):
        avg_of_a.append((a[count+1]+a[count])/2)                       # avg_of_a is a (1x23) list
        
    return(avg_of_a) 
    
def calcK(avg_of_a, pMax, pMin, W, B):
# this function, calcK(), intakes avg_of_a, pMax, pMin, W and B, and calculates the values of deltaK for each avg_of_a value. K is one row of the 2D array, array_of_K,
# which is what this function returns to. In the function call, a loop is used to execute through the 4 values of W and B, which is why the 2D array, array_of_K is (4x23) long 

    K = []                                                             

    for i in range (len(avg_of_a)):
        first = ((10**-6)*(pMax-pMin)*(np.sqrt(avg_of_a[i])))/(B*W)                                                                     # this is the first part of the calc             
        second = 30.96-(195.8*(avg_of_a[i]/W))+(730.6*(avg_of_a[i]/W)**2)-(1186.3*(avg_of_a[i]/W)**3)+(754.6*(avg_of_a[i]/W)**4)        # second part of the calc for K  
        K.append(first*second)                                         # K is equal to the product of first and second
        
    return(K)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def plot_K(da_dN,K):
# this function, plot_K(), intakes the lists of da_dN and array_of_K (called K for ease). This function will cycle through
# the 4 subplots using two for loops. The counter variable is to access the rows of array_of_K so that each row is plotted against the da_dN values. This is to then
# find the average of the 4 graph's slopes and intercepts (using curve-fitting function, np.ployfit) to relate these values to the A value and n values in Paris Equation.

    fig, ax=plt.subplots(2,2, figsize=(12,5))
    counter = 0  

    array_n = [0,0,0,0]                                               # array_n will contain the slope values from each of the 4 subplots
    array_A = [0,0,0,0]                                               # array_A will contain the 10^(y-intercept) values from each of the 4 subplots   
    for i in range(2):
        
        for j in range(2):
            
            x_vals_linear = np.array(K[counter])                      # converting row of K into numpy array
            y_vals_linear = np.array(da_dN)                           # converting da_dN into numpy array
            
            ax[i][j].scatter( K[counter] , (da_dN) ,c='black')        # plotting a scatter plot of each K vs. da_dN 
            
            slope, intercept = np.polyfit(np.log10(x_vals_linear), np.log10(y_vals_linear), 1)     # np.polyfit finds the slope and intercept from scatter plotted values 
            
            ax[i][j].plot((x_vals_linear), (10**(intercept))*(x_vals_linear)**slope )              # plotting Paris Equation in terms of K and da_dN  
            ax[i][j].set_xlabel("(K), Stress Intensity Factor")
            ax[i][j].set_ylabel("(da/dN), Crack Grow Rate")
            ax[0][0].set_title("Plot 1: the First set of K values vs. da/dN")
            ax[0][1].set_title("Plot 2: the Second set of K values vs. da/dN")
            ax[1][0].set_title("Plot 3: the Third set of K values vs. da/dN")
            ax[1][1].set_title("Plot 4: the Fourth set of K values vs. da/dN")
            
            ax[i][j].set_xscale('log')                              # log-log scale set for both axis
            ax[i][j].set_yscale('log')
            
            A_value = 10**(intercept)                               # because this is a log-log scale, the y-intercept = log(A), so to find A, a 10 power needs to be taken 
            
            array_n[counter] = (slope)
            array_A[counter] = (A_value)
            
            slope = round(slope, 3)
            
            ax[i][j].annotate(f'A = {A_value:.3e} n = {slope}', xy=(1, 0), xycoords='axes fraction', fontsize=10, xytext=(-5, 5), textcoords='offset points', ha='right', va='bottom')
            
            counter += 1
            
    mean_n, std_n, mean_A, std_A = get_mean_std(array_n, array_A)                  # this function call gets the average of the A and n Values, and the standard deviation for each
    print(f'The mean of n is {mean_n} and its standard deviation is {std_n}.')     
    print(f'The mean of A is {mean_A} and its standard deviation is {std_A}.')
    with open("Results.txt","a") as results:                                       # saving results to txt file
        results.write(f'The mean of n is {mean_n} and its standard deviation is {std_n}. \n')
        results.write(f'The mean of A is {mean_A} and its standard deviation is {std_A}. \n')
    
    fig.tight_layout(pad=2)
    plt.savefig("Subplots_for_B.pdf")                                             # saving subplots image to pdf file
    return ax

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_mean_std(array_n, array_A):
# this function, get_mean_std(), intakes the array_n and array_A calculated in the plot_K function. It uses np.std for the standard deviation
# and summing then diving by the length (4) for the mean. It returns the mean of A and n, as well as the standard deviation

    mean_n = round((sum(array_n))/len(array_n), 3)
    mean_A = format((sum(array_A))/len(array_A), "5.2e")

    std_n = round(np.std(array_n), 3)
    std_A = format(np.std(array_A), "5.2e" )
    
    return mean_n, std_n, mean_A, std_A
    






