import streamlit as st
import math
import pandas as pd

# Define the speeds and masses
speeds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]  # Velocity as a percentage of the speed of light
masses = [1, 10, 100, 1000, 10000]  # Mass in kilograms

# Create a DataFrame with the mass for each combination of mass and speed
data = {f"{speed * 100}% c": masses for speed in speeds}
df = pd.DataFrame(data)

# Display the DataFrame as a table
st.table(df)