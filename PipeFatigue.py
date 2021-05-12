# ENME 337, Final Project, Dec.9,2020, Kirsten Korsrud, Mazel Salve, Hamad Rizwan, Nicole Linares

import PartA
import PartB
import PartC

# This line creates a .txt file where the results of Problem A, Problem B, and Problem C are stored
# This is for the bonus marks (plots are also created)
results = open("Results.txt","w")
results.close()

# Our units are meters (m), Megapascals (MPa), days

def main():

    print('\n')
    print (35 * "-" , "MENU" , 37 * "-")                                                    # creating menu giving 4 options to user
    print ("Option 1. Part A: Pressure Surge Analysis")
    print ("Option 2. Part B: Determination of Crack Growth Rate Material Properties")
    print ("Option 3. Part C: Failure Probability Analysis")
    print ("Option 4. Exit")
    print (79 * "-")
    print('\n')

    userIn = int(input("Please input which menu option (1, 2, 3, or 4) you would like to run. NOTE: To choose another option from menu, close all figures beforehand. "))
    while userIn < 5:  # this is in order to loop through, so that the user can keep picking options off the menu without having to close each time

        if userIn == 1:
            PartA.mainA()
               
        if userIn == 2:
            PartB.mainB()
            
        if userIn == 3:
            PartC.mainC()
            
        elif userIn == 4:
            exit()

        print('\n')    
        userIn = int(input("Please input which menu option (1, 2, 3, or 4) you would like to run. NOTE: To choose another option from menu, close all figures beforehand. "))
        
main()      
      
    


