'''ENME 337, Assignment 5, Nov.11 2020, Kirsten Korsrud, kirsten.korsrud@ucalgary.ca'''
# please note that I organized my code according to Parts 1,2, and 3. (most) of the function calls are placed below the function definitions

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 1
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

num_nodes = 10
seg_length = 0.1

mat0 = np.arange(0,-(seg_length*2),-seg_length)                                           
maty = np.tile(mat0, int(num_nodes/2)).reshape(-1,1)                                # creating y values of node coordinates and inputting into num_nodes x 1 array
mat1 = np.arange(0,(seg_length*(num_nodes/2)),seg_length)                           # (the y coordinates follow the patturn of 0,-seg_length,0,-seg_length...)
matx = np.repeat(mat1,2).reshape(-1,1)                                              # creating x values of node coordinates and inputting into num_nodes x 1 array
                                                                                    # (the x coordinates follow the patturn of 0,0,seg_length,seg_length,seg_length*2,seg_length*2...)
beam_init = np.concatenate((matx,maty), axis=1)                                     # connecting the x and y coordinate arrays to create a num_nodes x 2 array, called beam_init
      
connect_matrix = np.eye(num_nodes,num_nodes, 2) + np.eye(num_nodes,num_nodes, 1)    # connectivity matrix shows which nodes are directly attached (denoted by 1) and are not (denoted by 0)
    
plt.imshow(connect_matrix)                                                          # visual of the connectivity matrix, yellow indicates attached, and purple indicates not connected 

initial_length = connect_matrix * seg_length                                        # initial_length is an array that stores the lengths of only the directly connected nodes

for i in range(1,num_nodes,2):
    for j in range(2,num_nodes,2):
        if initial_length[i][j] != 0:
            initial_length[i][j] = ((seg_length**2)*2)**0.5                         # the nodes that are connected by a diagonal segment have use pythagorean theorem to find distance
            
'''----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
''' Distance Function '''
            
def calc_distance (beam_init):
# calc_distance intakes a num_nodes x 2 array containing the x and y node coordinates, and returns a num_nodes x num_nodes array containing the distances between each node
# this is done by using the Eclidian distance formula, where the outputted array is assigned to dist_array

    arrayX = beam_init[:,0]                                                         # the x values of beam_init are cycled through and inputted into arrayX   
    p1 = arrayX[:, np.newaxis]                                                      # arrayx is converted from 1D array to a 2D one and assigned to p1

    p2 = beam_init[:,0]                                                             # the x values of beam_init are cycled through and assigned to p2 
        
    xdiff = (p1-p2)**2                                                              # broadcasting is used to find the difference between in x coordinates and assigned to array xdiff
    
    arrayY = beam_init[:,1]                                                         # ^^ this exact process is done for the difference between y coordinates
    q1 = arrayY[:, np.newaxis]

    q2 = beam_init[:,1]

    ydiff = (q1-q2)**2                                                              # broadcasting is used to find the difference between y coordinates and assigned to array ydiff 
    
    dist_array = (xdiff+ydiff)**(0.5)                                               # dist_array stores the square root (sum of xdiff and ydiff)
    
    return dist_array

'''----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
''' Plotting Function '''

def plot_system(dist, initial_length, beam):
# plot_system intakes array of distances, array of initial lengths, and array of node coordinates, and returns the ax object. This function plots the nodes and segments of the beam
# and colours the beam segments according the experienced tension and compression. This function is called twice, once for plotting the intial unchanged lengths of the beam, and
# again to plot the beam incorporating the potential energy experienced.

    fig, ax = plt.subplots(1,1)                                                     # creating axes object to graph 
    plt.axis('off')                                                                 # x and y axis are turned off
    
    arrzip = np.nonzero(connect_matrix)                                             # arrzip is a num_nodes x 2 array that takes out all the indecies of connect_matrix that have non-zero values 
    I = arrzip[0]                                                                   # I is a 'column vector' array containing the outer indecies  
    J = arrzip[1]                                                                   # J is a 'column vector' array containing the inner indecies
   
    elongs = np.array([dist[i, j] - initial_length[i, j] for i, j in zip(I, J)])  # elongs is a 'row vector' array containing the differences in initial length of segment to the new distance of segment 
    
    seg_length_change_max = np.abs(elongs).max()                                    # seg_length_change_max contains the absolute value of maximum elongs value 
   
    colourarr = np.zeros(((2*num_nodes)-3,4))                                       # colourarr is a (length of elongs) x 4 array which will store RGBA values for colour
    colourarr[:,-1] = 1
    
    if seg_length_change_max > 1e-10:                                               # this condition is to check that seg_length_change_max is greater than 1e-10 because this is essentially zero
        
        elongs /= seg_length_change_max                                             # Normalizing elongs values 
        
        pos, neg, = elongs > 0, elongs < 0
        colourarr[pos] = plt.cm.inferno(elongs[pos])                                # assigning the tension values to inferno colour map in colouarr 
        colourarr[neg] = plt.cm.bone(-elongs[neg])                                  # assigning the compression values to bone colour map in colourarr
        
    for i, j, c in zip(I, J, colourarr):                                            # plotting system, colour c corresponds to colourarr tension/ compress values, 
        ax.plot(beam[[i, j], 0], beam[[i, j], 1], lw=2, color=c)                    # and having all zeros if the beam is not either, which is black
        
    ax.scatter(beam[:,0], beam[:,1],color='black')                                  # plotting nodes of beam
    plt.axvline(color='black')
    
    
    plt.axis('equal')                                                               # equliizing size of figure so beam looks to have square components
    
    return ax

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 2
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
''' Energy Function '''

def energy_calc(beam):
# energy_calc intakes an array of node coordinates and outputs the total potential energy of the beam. This is done by summing the graviational energy Eg, and
# the elastic potential energy Es for all of the nodes. The arrays connect_matrix, initial_length, and calc_distance function to find distances are used within the function as well.

    m = 0.5
    g = 9.81
    k = 10000
    
    beam = beam.reshape((-1, 2))                                       
    
    D = calc_distance(beam)                                                        # finding distances between node coordinates 

    C = connect_matrix
    L = initial_length

    Eg = m*g*beam[:,1]                                                             # gravitional energy calculation
    Es = k*C*((D-L)**2)                                                            # elastic energy calculation
    
    return (np.sum(Eg)+(0.5*np.sum(Es)))                                           # summing energies (and diving sum of elastic by 2) per formula


num_nodes_fixed = 2
sample_bounds = np.c_[beam_init[:num_nodes_fixed, :].ravel(),                      
               1e-10 + beam_init[:num_nodes_fixed, :].ravel()].tolist() \
               + [[None, None]] * (2 * (num_nodes - num_nodes_fixed))
# sample_bounds is an array specifying the max and min values for each coordinate. By prestating that    
# the first 2 nodes are fixed, they have maximum and min values so the beam is always connected to wall 

energy_equil = opt.minimize(energy_calc,beam_init.ravel(),method='L-BFGS-B',bounds=sample_bounds).x.reshape((-1, 2))
# energy_equil is an array that stores the equilibrated node coordinates considering energy by using opt.minimize. It intakes beam_init and uses energy_calc to get potential energy.
# these values are then is used to be plotted to show the energy compression/ tension diagram

dist_array = calc_distance(beam_init)                                              # function call to calc distances for initial node coordinates  

energy_dist = calc_distance(energy_equil)                                          # function call to calc distances for energy node coordinates

ax = plot_system(dist_array, initial_length, beam_init)                            # function call for initial beam diagram
ax.set_title("Initial Beam Compression/Tension Diagram")

axx = plot_system(energy_dist, initial_length, energy_equil)                       # function call for energy beam diagram
axx.set_title("Beam Compression/Tension Diagram With Potential Energy")

energy_value = energy_calc(beam_init)                                              # function call to calc potential energy of system

print('The energy of the beam is: ', energy_value)

plt.show()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 3
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# a) the total energy is -73.575 J
# b) I am defining the beam to be 'unphysical' when it deviates >45 degrees from the horizontal configuration.
#    This is because looking at the system and tension in the first 2 attached segments, the beam would realistically
#    not be able to support the weigth of the structure and would snap after ~45 degrees. The max value of g is ~ 2 m/s^2
#    because greater than this and the beam bends more than 45 degrees
# c) k needs to be increased from 1000 to ~25,000 to return to a nearly horizontal state (guess and check method)
# d) the total energy is -4.905 J when changing num_nodes_fixed to 6, and num_nodes = 20, compared to 2 fixed nodes and num_nodes = 10 the energy was -2.4525 J
# e) the parameter that had the greatest effect on the beam (from the configuration) was the seg_length value. Realistically, this makes sense because increase the length of
#    each segment increase the overall size of the stucture, making it more difficult for the beam to support the weight. Increasing the seg_length caused an increase in potential
#    energy, as the y-coordinate distance for each node increased, whereas changing a constant value (such as m, g, or k) applies to the overall system instead of each node, not
#    having that great of an effect. 

   

