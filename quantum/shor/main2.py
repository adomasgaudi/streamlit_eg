import streamlit as st
from functions2 import run_shors_algorithm, plot_histogram

# Constants
N_COUNT = 8  # Number of counting qubits
A_VALUE = 7  # Specific value for the algorithm
N = 15       # Number to be factored

# Set the title of the Streamlit app
st.title("Shor's Algorithm Simulator")

# Main Streamlit app logic
if st.button('Run Quantum Circuit'):
    # Run Shor's algorithm
    r, guesses, histogram_data, df = run_shors_algorithm(N_COUNT, A_VALUE, N)
    
    # Display the results
    st.write(f"Result: r = {r}")
    st.write(f"Guessed Factors: {guesses[0]} and {guesses[1]}")
    st.write(df)

    # Display the histogram
    plot_histogram(histogram_data)
