import streamlit as st
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

st.title("Wigner's friend Quantum Circuit")
# some text
st.write("""
In quantum mechanics, Wigner's friend is a thought experiment proposed by the physicist Eugene Wigner to
highlight the paradoxical nature of quantum measurement and the questions that it brings up about which
observer plays a privileged role in the universe. The scenario involves two observers: Wigner's friend
and Wigner himself. Wigner's friend is inside a laboratory and performs a measurement on a qubit. Wigner
is outside the laboratory and does not know the result of the measurement. The state of the qubit and
the measurement apparatus is a quantum superposition of "friend saw 0" and "friend saw 1", which is
entangled with the state of Wigner and the laboratory. Wigner can describe this state as a quantum
superposition of "friend saw 0 and Wigner saw friend saw 0" and "friend saw 1 and Wigner saw friend saw 1".
""")

# Create quantum registers and circuit
qr1 = QuantumRegister(1, name="System qubit")
qr2 = QuantumRegister(1, name="Wigner's friend")
cr1 = ClassicalRegister(1, name="Wigner's friend's outcome")
# qr_atom = QuantumRegister(1, name="atom")
# qr_cat = QuantumRegister(1, name="cat")
# qr_observer = QuantumRegister(1, name="observer")
# qc = QuantumCircuit(qr_atom, qr_cat, qr_observer)

# Build the quantum circuit
# qc.h(qr_atom[0])
# qc.cx(qr_atom[0], qr_cat[0])
# qc.cx(qr_cat[0], qr_observer[0])

qc = QuantumCircuit(qr1, qr2, cr1)
qc.h(0)
qc.cx(0,1)
# Draw the circuit
qc.measure_all()
figure = qc.draw("mpl")
figure.savefig("circuit.png")
st.image("circuit.png")

def runIBMButton():
    if st.button('Run Quantum Circuit'):
        # Execute the quantum circuit
        backend = AerSimulator()
        result = backend.run(qc, shots=100000).result()

        figure2 = plot_histogram(result.get_counts())
        figure2.savefig("circuit2.png")
        st.image("circuit2.png")
        st.write(result.get_counts())

runIBMButton()