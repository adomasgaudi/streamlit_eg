import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from io import BytesIO


def format_energy(energy):
    """
    Converts energy value to LaTeX formatted scientific notation.

    Args:
    energy (float): The energy value to format.

    Returns:
    str: The formatted energy string in LaTeX notation.
    """
    energy_sci = f"{energy:.1e}"
    base, exponent = energy_sci.split("e")
    exponent = exponent.lstrip("+")
    latex_string = f"{base} \\times 10^{{{exponent}}}"
    return latex_string
    # return energy_sci
    # return base + "-" + exponent

def calculate_kinetic_energy(m, v_percent):
    """
    Calculates the relativistic kinetic energy.

    Args:
    m (float): Mass in kilograms.
    v_percent (float): Velocity as a percentage of the speed of light.

    Returns:
    float or str: The kinetic energy or 'Infinity' if velocity equals or exceeds light speed.
    """
    c = 3.0e8  # Speed of light in meters per second
    v = v_percent * c
    if v >= c:
        return "Infinity"
    gamma = 1 / math.sqrt(1 - v**2 / c**2)
    return m * c**2 * (gamma - 1)

def display_kinetic_energy_table():
    """
    Displays a table of kinetic energy calculations for various masses and velocities.
    """
    st.title("Kinetic Energy Calculation Table")

    # Define a range of masses and velocities
    masses = [1000, 2000, 3000]  # in kg
    velocities = [0.5, 0.7, 0.9]  # as a fraction of the speed of light

    # Create and display the table
    st.write("Mass (kg)", "Velocity (% of c)", "Kinetic Energy (Joules)")
    for mass in masses:
        for v_percent in velocities:
            kinetic_energy = calculate_kinetic_energy(mass, v_percent)
            kinetic_energy_latex = format_energy(kinetic_energy)
            st.write(mass, v_percent * 100, kinetic_energy, kinetic_energy_latex)
            st.write(mass, v_percent * 100, kinetic_energy_latex)
            st.latex(kinetic_energy_latex)


# display_kinetic_energy_table()


st.latex('1.1 \\times 10^{20}')
# efine the speeds and masses
# speeds = ['0.2c', '0.3c', '0.4c', '0.5c', '0.6c', '0.7c', '0.8c', '0.9c', '0.99c']  # Velocity as a percentage of the speed of light
# masses = ['1kg', '10kg', '100kg', '1000kg', '10000kg']  # Mass in kilograms

# # Create a DataFrame with the LaTeX string for each combination of mass and speed
# data = {speed: [st.latex(f'$1.1 \\times 10^{{20}}') for mass in masses] for speed in speeds}
# df = pd.DataFrame(data)

# # Display the DataFrame as a table
# st.table(df)

# Define the speeds and masses


# Define the speeds and masses
speeds = ['0.2c', '0.3c', '0.4c', '0.5c', '0.6c', '0.7c', '0.8c', '0.9c', '0.99c']  # Velocity as a percentage of the speed of light
masses = ['1kg', '10kg', '100kg', '1000kg', '10000kg']  # Mass in kilograms

# Create a DataFrame with the LaTeX string for each combination of mass and speed
data = {speed: [f'$1.1 \\times 10^{{20}}$ {mass}' for mass in masses] for speed in speeds}
df = pd.DataFrame(data)

# Create a new figure with a larger size
fig, ax = plt.subplots(figsize=(20, 20))

# Hide axes
ax.axis('off')

# Create a table and add it to the figure
cell_colours = [["w"]*len(df.columns) for _ in range(len(df))]
table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center', cellColours=cell_colours)

# Increase the font size
table.auto_set_font_size(False)
table.set_fontsize(14)

# Increase cell size
table.scale(2, 4)

# Save the figure to a BytesIO object
buf = BytesIO()
plt.savefig(buf, format='png')

# Rewind the buffer to the beginning
buf.seek(0)

# Display the image in Streamlit
st.image(buf)