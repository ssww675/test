import numpy as np
import matplotlib.pyplot as plt
from image_process import delete_files_in_root_folder

#Example array of strings
##string_array = ["+10, 0", "-10, 2500","-10,7500", "+10, 10000"]

    
def calculations(string_array):
    delete_files_in_root_folder(['bending_moment_graph.jpeg'])
    print("calculation started \n values are : \n")
    print(string_array)
    
    # Initialize empty lists to store the split values
    x_input = []
    y_input = []

    shear_y = []
    shear_x = []

    # Loop through each string in the array
    for string in string_array:
        print(string)
        # Split the string at the comma
        split_values = string.split(",")

        # Add the first value to the first_values list
        y_input.append(int(split_values[0]))

        # Add the second value to the second_values list
        x_input.append(int(split_values[1])/1000)



    def generate_shearforce_cordinates(x_input, y_input):
        y =[]
        cum_y = 0
        for value in range(len(y_input)):
            cum_y = cum_y + y_input[value]
            y.append(cum_y)
        
        for val in range (len(y)):
            if(val == len(y)-1):
                shear_y.append(y[val])
            else:
                shear_y.append(y[val])
                shear_y.append(y[val])

        for val in range (len(x_input)):
            if(val == 0):
                shear_x.append(x_input[val])
            else:
                shear_x.append(x_input[val])
                shear_x.append(x_input[val])
                
        return shear_x , shear_y



    def generate_bending_cordinates(x,y):

        lengths = []
        val_for_bending = []
        y_for_bending = []

        for value in range(len(x)):
            if (value + 1 < len(x)):
                lengths.append(x[value + 1] - x[value])

        for val in range(len(y)):
            if (val < len(y) - 1):
                val_for_bending.append(lengths[val] * y[val])

        cumil = 0
        for val in range(len(val_for_bending)):
            if (val > 0):
                cumil = cumil + val_for_bending[val] 
                y_for_bending.append(cumil)
            else:
                cumil = cumil + val_for_bending[val] 
                y_for_bending.append(0)
                y_for_bending.append(val_for_bending[val])

        return (y_for_bending)

    # convert the lists to numpy arrays
    def plot(diagram_name, x_name, y_name, x, y):


        x_array = np.array(x)
        y_array = np.array(y)

        # plot the graph using matplotlib
        plt.plot(x_array, y_array)

        plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')

        # set the axis labels and title
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.title(diagram_name)

        # display the graph
        plt.savefig('bending_moment_graph.jpeg', dpi=300)

        #plt.show()

    temp =[]

    x,y =generate_shearforce_cordinates(x_input,y_input)



    x.insert(0, 0)
    y.insert(0, 0)
    plot("Shear Force Diagram", "x(m)", "Shear Force(Nm)", x, y)


    temp_y = []
    cum_y = 0
    for value in range(len(y_input)):
        cum_y = cum_y + y_input[value]
        temp_y.append(cum_y)


    plot("Shear Force and Bending Moment Diagram","x(m)", "Bending Moment(Nm)/ Shear Force(N)", x_input, generate_bending_cordinates(x_input,temp_y))

calculations(["+10, 0", "-10, 2500","-10,7500", "+10, 10000"])