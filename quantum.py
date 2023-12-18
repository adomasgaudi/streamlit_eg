import streamlit as st
import math
import pandas as pd

import streamlit as st
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.providers.ibmq import least_busy
from qiskit import IBMQ
from qiskit.visualization import plot_bloch_multivector, plot_histogram
# Define the speeds and masses
speeds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]  # Velocity as a percentage of the speed of light
masses = [1, 10, 100, 1000, 10000]  # Mass in kilograms

# Create a DataFrame with the mass for each combination of mass and speed
data = {f"{speed * 100}% c": masses for speed in speeds}
df = pd.DataFrame(data)

# Display the DataFrame as a table
st.table(df)

# Load IBM Q account
IBMQ.load_account()

# Define a quantum circuit for multiplication
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.draw('mpl')

# Display the quantum circuit
st.write(qc)

# Explanation
st.write("""
This is a simple quantum circuit that applies a Hadamard gate to the first qubit (putting it into a superposition of states), 
and then a CNOT gate (controlled NOT gate) with the first qubit as control and the second as target. 
The result is an entangled state where the state of the second qubit is always the same as the state of the first qubit.
""")

# Button to run the circuit on a quantum computer
if st.button('Run on Quantum Computer'):
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and not x.configuration().simulator and x.status().operational==True))
    transpiled_circuit = transpile(qc, backend, optimization_level=3)
    qobj = assemble(transpiled_circuit)
    job = backend.run(qobj)
    
    # Get the result and display it
    result = job.result()
    st.write(result.get_counts())