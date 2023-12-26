import streamlit as st
import math

def format_energy(joules):
    units = ["", "Kilo", "Mega", "Giga", "Tera", "Peta", "Exa"]
    thresholds = [1, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18]  # Corresponding values for Kilo, Mega, Giga, etc.

    for i in range(len(thresholds)):
        if joules < thresholds[i]:
            unit = units[i - 1]
            value = joules / thresholds[i - 1]
            return f"{value:.2f} {unit}"
    return f"{joules} Joules"  # Default case for extremely large numbers

# Function to calculate kinetic energy
def calculate_kinetic_energy(m, v_percent):
    c = 3.0e8  # Speed of light in meters per second
    v = v_percent * c  # Velocity as a percentage of the speed of light
    gamma = 1 / math.sqrt(1 - v**2 / c**2)
    KE = m * c**2 * (gamma - 1)
    st.write(f"Kinetic Energy: {format_energy(KE)} Joules")

st.set_page_config(page_title="steamlit" ,page_icon=":smiley:" ,layout="wide" ,initial_sidebar_state="expanded")

st.title("Kinetic Energy Calculator")
st.subheader("Calculate the kinetic energy of an object moving at a fraction of the speed of light")
st.write("""
Enter the mass of the object in kilograms and its velocity as a percentage of the speed of light.
Then click 'Calculate' to see the kinetic energy of the object.
""")

# Create two number inputs
mass_input = st.number_input('Mass (kg):', value=1.0)
velocity_input = st.slider('Velocity (% of c):', min_value=0.0, max_value=1.0, value=0.1, step=0.01)

# Create a button, when clicked, the kinetic energy is calculated
if st.button('Calculate'):
    calculate_kinetic_energy(mass_input, velocity_input)