import streamlit as st
from functions import setup_shors_algorithm_circuit, run_quantum_circuit

# Constants
MY_TOKEN = 'd79a58cef57641543701b758b34f4eab6b344d1d52a9e18e3d42695dc153028be326695f1388c5b276d36c4a963d1ba15be8ed096a3cfe79be3559411529758c'
N_COUNT = 8  # Number of counting qubits
A_VALUE = 7  # Specific value for the algorithm


# Set the title of the Streamlit app
st.title("Shor's Algorithm")

# Main Streamlit app logic
if st.button('Run Quantum Circuit'):
    qc = setup_shors_algorithm_circuit(N_COUNT, A_VALUE)
    run_quantum_circuit(qc, N_COUNT)