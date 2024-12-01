import numpy as np

def vector_sum(n):
    # Define each angle in radians, evenly spaced around the circle
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # Calculate x and y components of each vector
    x_components = np.cos(angles)
    y_components = np.sin(angles)
    # Sum up the x and y components
    total_x = np.sum(x_components)
    total_y = np.sum(y_components)
    # Resultant vector sum
    return total_x, total_y
# Example with 12 vectors (you can change n to test different values)
n = 15
result = vector_sum(n)
print(f"Resultant vector sum: ({result[0]:.2e}, {result[1]:.2e})")