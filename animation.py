import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle as pk
# Function to calculate the hyperplane equation for 3D space
def hyperplane_equation(x, y, a, b, c):
    return a * x + b * y + c

# Initialize your reinforcement learning environment and simulation here
# ...

# Create a figure for 3D plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize the hyperplane coefficients
a, b, c = 1.0, 2.0, 3.0

# Create grids of var1 and var2
var1_values = np.linspace(0, 100, 5)  # Define min, max, and num_points
var2_values = np.linspace(0, 100, 5)  # Define min, max, and num_points
var1_grid, var2_grid = np.meshgrid(var1_values, var2_values)

# Initialize the previous values for the two variables
prev_var1, prev_var2 = 6.86, 2.3  # Replace with initial values

# Function to update the plot for each time step
file_time_out="C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//test_files//time_out_state.pkl"
time_out = []
with open(file_time_out, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            time_out.append(loaded_value)
    except EOFError:
        pass

for i in time_out:
    print(i)
def update_plot(index):
    global a, b, c, prev_var1, prev_var2

    # Get the value from time_out list using the index
    time_out_value = time_out[index]

    # Generate random values for var1 and var2
    var1 = time_out_value[2]
    var2 = time_out_value[3]
    # print(var1)
    # print(var2)
    # Update the hyperplane coefficients based on prev_var1 and prev_var2
    a = prev_var1
    b = prev_var2
    c = np.random.choice([0,1])

    # Calculate the hyperplane equation with the updated coefficients
    z = hyperplane_equation(var1_grid, var2_grid, a, b,c)

    # Plot the hyperplane in 3D space
    ax.clear()
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ax.set_zlabel('Hyperplane')
    ax.plot_surface(var1_grid, var2_grid, z, cmap='viridis')

    # Store the current variable values as previous for the next iteration
    prev_var1, prev_var2 = var1, var2

# Create the animation and store it in a variable
# Pass the range of indices of time_out list as frames
ani = FuncAnimation(fig, update_plot, frames=len(time_out), repeat=False)

# Display the animation
plt.show()
