#!/usr/bin/python

## Massimiliano Patacchiola, Plymouth University 2016
#
# This code uses Self-Organizing Map (SOM) to classify six colours.
# For each epoch it is possible to save an image which represents the weights of the SOM.
# Each weight is a 3D numpy array with values ranging between 0 and 1. The values can be converted
# to RGB in the range [0,255] and then displayed as colours.
# You can use avconv to convert the images to a video: avconv -f image2 -i %d.png -r 12 -s 800x600 output.avi
# The name of the images must be in order, if there is one or more missing names (ex: 18.png, 25.png) 
# an empty video will be created.
# At the end of the example the network is saved inside the file: examples/som_colours.npz

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os 

#It requires the pyERA library
from pyERA.som import Som
from pyERA.utils import ExponentialDecay
from pyERA.utils import LinearDecay


def main():

    #Set to True if you want to save the SOM images inside a folder.
    SAVE_IMAGE = True
    output_path = "./output/" #Change this path to save in a different forlder
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #Init the SOM
    som_size = 512
    my_som = Som(matrix_size=som_size, input_size=3, low=0, high=1, round_values=False)
    
    #Init the parameters
    tot_epoch = 1500
    my_learning_rate = ExponentialDecay(starter_value=0.4, decay_step=50, decay_rate=0.9, staircase=True)
    my_radius = ExponentialDecay(starter_value=np.rint(som_size/3), decay_step=80, decay_rate=0.90, staircase=True)

    #Starting the Learning
    for epoch in range(1, tot_epoch):

        #Saving the image associated with the SOM weights
        if(SAVE_IMAGE == True):
            img = np.rint(my_som.return_weights_matrix()*255)
            plt.axis("off")
            plt.imshow(img)
            plt.savefig(output_path + str(epoch) + ".png", dpi=None, facecolor='black')

        #Updating the learning rate and the radius
        learning_rate = my_learning_rate.return_decayed_value(global_step=epoch)
        radius = my_radius.return_decayed_value(global_step=epoch)

        #Generating random input vectors
        colour_selected = np.random.randint(0, 6)
        colour_range = np.random.randint(100, 255)
        colour_range = float(colour_range) / 255.0
        if(colour_selected == 0): input_vector = np.array([colour_range, 0, 0]) #RED
        if(colour_selected == 1): input_vector = np.array([0, colour_range, 0]) #GREEN
        if(colour_selected == 2): input_vector = np.array([0, 0, colour_range]) #BLUE
        if(colour_selected == 3): input_vector = np.array([colour_range, colour_range, 0]) #YELLOW
        if(colour_selected == 4): input_vector = np.array([0, colour_range, colour_range]) #LIGHT-BLUE
        if(colour_selected == 5): input_vector = np.array([colour_range, 0, colour_range]) #PURPLE

        #Estimating the BMU coordinates
        bmu_index = my_som.return_BMU_index(input_vector)
        bmu_weights = my_som.get_unit_weights(bmu_index[0], bmu_index[1])

        #Getting the BMU neighborhood
        bmu_neighborhood_list = my_som.return_unit_round_neighborhood(bmu_index[0], bmu_index[1], radius=radius)  

        #Learning step      
        my_som.training_single_step(input_vector, units_list=bmu_neighborhood_list, learning_rate=learning_rate, radius=radius, weighted_distance=False)

        print("")
        print("Epoch: " + str(epoch))
        print("Learning Rate: " + str(learning_rate))
        print("Radius: " + str(radius))
        print("Input vector: " + str(input_vector*255))
        print("BMU index: " + str(bmu_index))
        print("BMU weights: " + str(bmu_weights*255))
        #print("BMU NEIGHBORHOOD: " + str(bmu_neighborhood_list))


    #Saving the network
    file_name = output_path + "som_colours.npz"
    print("Saving the network in: " + str(file_name))
    my_som.save(path=output_path, name="some_colours")

    img = np.rint(my_som.return_weights_matrix()*255)
    plt.axis("off")
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    main()
