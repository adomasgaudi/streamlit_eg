import streamlit as st
import math

# Constants
g = 10  # Approximation of gravitational acceleration for simplicity

def calculate_max_speed(energy_density_j_kg, cost_EUR_ton, total_money_EUR, dry_mass_ton=1000, efficiency=0.5):
    """
    Calculate the maximum speed a rocket can reach, considering both fuel and dry mass.

    :param energy_density_j_kg: Energy density of the fuel (in J/kg)
    :param cost_EUR_ton: Cost of the fuel per tonne (in EUR/tonne)
    :param total_money_EUR: Total money available for fuel (in EUR)
    :param dry_mass_ton: Dry mass of the rocket (in tonnes)
    :param efficiency: Efficiency of the rocket engine (default 50%)
    :return: Maximum speed (in m/s)
    """
    # Calculate total mass of fuel that can be bought in tonnes
    fuel_mass_ton = total_money_EUR / cost_EUR_ton

    # Convert dry mass and fuel mass to kilograms
    dry_mass_kg = dry_mass_ton * 1000
    fuel_mass_kg = fuel_mass_ton * 1000

    # Calculate the total energy available from the fuel in joules
    total_energy_j = fuel_mass_kg * energy_density_j_kg * efficiency

    # Calculate the initial total mass of the rocket (dry mass + fuel mass) in kilograms
    initial_total_mass_kg = dry_mass_kg + fuel_mass_kg

    # Calculate maximum speed using kinetic energy formula (assuming all energy is converted to kinetic energy)
    max_speed_m_s = math.sqrt((2 * total_energy_j) / initial_total_mass_kg)

    return max_speed_m_s

def calculate_time_distance(max_speed, acceleration=g):
    """
    Calculate the time and distance to reach the maximum speed at 1g.

    :param max_speed: Maximum speed (in m/s)
    :param acceleration: Acceleration (default 1g, in m/s^2)
    :return: Time (in seconds) and distance (in meters) to reach the maximum speed
    """
    # Calculate the time to reach maximum speed
    time_to_max_speed = max_speed / acceleration

    # Calculate the distance covered to reach maximum speed
    distance_covered = 0.5 * acceleration * time_to_max_speed ** 2

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
    "Low Cost": 2000,  # EUR/tonne
    "Medium Cost": 5000,  # EUR/tonne
    "High Cost": 16000  # EUR/tonne
}
total_money_options = {
    "10B EUR": 10000000000,
    "50B EUR": 50000000000,
    "100B EUR": 100000000000
}

# Function to format options for display
def format_options(options_dict):
    return [f"{key} - {value}" for key, value in options_dict.items()]

# Creating selection boxes for user input
options_dict = {
    "Select the type of fuel": energy_density_options,
    "Select the price range of the fuel": price_per_tonne_options,
    "Select the total money available for fuel": total_money_options
}
selections = {label: st.selectbox(label, format_options(options)) for label, options in options_dict.items()}

# Calculate button
if st.button('Calculate Maximum Speed'):
    # Extracting the selected options
    energy_density_key = selections["Select the type of fuel"].split(" - ")[0]
    price_per_tonne_key = selections["Select the price range of the fuel"].split(" - ")[0]
    total_money_key = selections["Select the total money available for fuel"].split(" - ")[0]

    # Performing the maximum speed calculation
    max_speed = calculate_max_speed(
        energy_density_options[energy_density_key], 
        price_per_tonne_options[price_per_tonne_key], 
        total_money_options[total_money_key]
    )

    # Calculating time and distance to reach maximum speed
    time_to_max_speed, distance_covered = calculate_time_distance(max_speed)

    # Displaying the results
st.write(f"The maximum speed the rocket can reach is {max_speed:.2f} m/s.")
st.write(f"Time to reach maximum speed at 1g acceleration: {time_to_max_speed:.2f} seconds.")
st.write(f"Distance covered to reach maximum speed at 1g acceleration: {distance_covered:.2f} meters.")
