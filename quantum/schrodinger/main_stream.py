import streamlit as st
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

st.title("Schrodinger's Cat")
st.title("Quantum Circuit")

# Create quantum registers and circuit
qr_atom = QuantumRegister(1, name="atom")
qr_cat = QuantumRegister(1, name="cat")
qr_observer = QuantumRegister(1, name="observer")
qc = QuantumCircuit(qr_atom, qr_cat, qr_observer)

# Build the quantum circuit
qc.h(qr_atom[0])
qc.cx(qr_atom[0], qr_cat[0])
qc.cx(qr_cat[0], qr_observer[0])

# Draw the circuit
qc.measure_all()
figure = qc.draw("mpl")
figure.savefig("circuit.png")
st.image("circuit.png")

def runIBMButton():
    if st.button('Run Quantum Circuit'):
        # Execute the quantum circuit
        backend = AerSimulator()
        result = backend.run(qc, shots=100).result()
        st.write(result.get_counts())

runIBMButton()