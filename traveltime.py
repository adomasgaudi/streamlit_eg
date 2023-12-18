import streamlit as st
import math

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)

# Function to calculate maximum speed
def calculate_max_speed(energy_density, price_per_tonne, total_money, efficiency=0.5):
    """
    Calculate the maximum speed a rocket can reach.

    :param energy_density: Energy density of the fuel (in J/kg)
    :param price_per_tonne: Price of the fuel per tonne
    :param total_money: Total money available for fuel
    :param efficiency: Efficiency of the rocket engine (default 50%)
    :return: Maximum speed (in m/s)
    """
    # Calculate total mass of fuel that can be bought
    mass_of_fuel = (total_money / (price_per_tonne * 1000))  # in kilograms

    # Calculate total energy available from the fuel
    total_energy = mass_of_fuel * energy_density * efficiency

    # Use kinetic energy formula: KE = 0.5 * m * v^2
    # Assume the mass of the rocket is small compared to the fuel mass for simplicity
    max_speed = math.sqrt((2 * total_energy) / mass_of_fuel)
    return max_speed

# Function to calculate time and distance to reach max speed at 1g
def calculate_time_distance(max_speed, acceleration=g):
    """
    Calculate the time and distance to reach the maximum speed at 1g.

    :param max_speed: Maximum speed (in m/s)
    :param acceleration: Acceleration (default 1g, in m/s^2)
    :return: Time (in seconds) and distance (in meters) to reach the maximum speed
    """
    time_to_max_speed = max_speed / acceleration  # Time = Speed / Acceleration
    distance_covered = 0.5 * acceleration * time_to_max_speed ** 2  # Distance = 0.5 * Acceleration * Time^2
    return time_to_max_speed, distance_covered

# Streamlit user interface
st.title("Rocket Maximum Speed Calculator")

# Predefined options for inputs
energy_density_options = {
    "Liquid Hydrogen": 14200000,  # J/kg
    "RP-1 (Rocket Propellant-1)": 46000000,  # J/kg
    "Methane": 55900000  # J/kg
}
price_per_tonne_options = {
    "Low Cost": 200,  # $/tonne
    "Medium Cost": 500,  # $/tonne
    "High Cost": 1000  # $/tonne
}
total_money_options = {
    "10B $": 10000000000,
    "50B $": 50000000000,
    "100B $": 100000000000
}

def format_options(options_dict):
    return [f"{key} - {value}" for key, value in options_dict.items()]

options_dict = {
    "Select the type of fuel": energy_density_options,
    "Select the price range of the fuel": price_per_tonne_options,
    "Select the total money available for fuel": total_money_options
}

selections = {label: st.selectbox(label, format_options(options)) for label, options in options_dict.items()}

# Button to perform calculation
if st.button('Calculate Maximum Speed'):
    # Extract the keys from the selected options
    energy_density_key = selections["Select the type of fuel"].split(" - ")[0]
    price_per_tonne_key = selections["Select the price range of the fuel"].split(" - ")[0]
    total_money_key = selections["Select the total money available for fuel"].split(" - ")[0]

    max_speed = calculate_max_speed(
        energy_density_options[energy_density_key], 
        price_per_tonne_options[price_per_tonne_key], 
        total_money_options[total_money_key]
    )

    # Calculate time and distance
    time_to_max_speed, distance_covered = calculate_time_distance(max_speed)
    st.write(f"The maximum speed the rocket can reach is {max_speed:.2f} m/s.")
    st.write(f"Time to reach maximum speed at 1g acceleration: {time_to_max_speed:.2f} seconds.")
    st.write(f"Distance covered to reach maximum speed at 1g acceleration: {distance_covered:.2f} meters.")
