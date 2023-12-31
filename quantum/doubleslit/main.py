import streamlit as st

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator

import numpy as np 
import matplotlib.pyplot as plt 



simulator = AerSimulator()

π = np.pi
φ = Parameter('φ')

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.p(φ, 0)
qc.h(0)
qc.measure(0, 0)
qc.draw('mpl')






st.title("Double Slit Experiment")
# some text
st.write("""
The double-slit experiment is a demonstration that light and matter can display characteristics of both
classically defined waves and particles; moreover, it displays the fundamentally probabilistic nature of
quantum mechanical phenomena. The experiment was first performed with light by Thomas Young in 1801.
""")




# measure


# Draw the circuit

if st.button('Run Quantum Circuit'):
    figure = qc.draw("mpl")
    figure.savefig("circuit.png")
    st.image("circuit.png")

# def runIBMButton():
        # Execute the quantum circuit
        # backend = AerSimulator()
        # qc_transpiled = transpile(qc, backend)

        # result = backend.run(qc_transpiled, shots=1000).result()

        # figure2 = plot_histogram(result.get_counts())
        # figure2.savefig("circuit2.png")
        # st.image("circuit2.png")
        # st.write(result.get_counts())

# runIBMButton()