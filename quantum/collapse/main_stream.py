import streamlit as st
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library.standard_gates import XGate

st.title("Many worlds vs Copenhagen interpretation")
# some text
st.write("""
The many-worlds interpretation (MWI) is an interpretation of quantum mechanics that asserts that the
universal wavefunction is objectively real, and that there is no wavefunction collapse. This implies
that all possible outcomes of quantum measurements are physically realized in some "world" or universe.
""")

# Create quantum registers and circuit
qr1 = QuantumRegister(1, name="Coin qubit")
qr2 = QuantumRegister(1, name="Observer")
qr3 = QuantumRegister(1, name="Record")
# cr1 = ClassicalRegister(1, name="Record")

qc = QuantumCircuit(qr1, qr2, qr3)
qc.h(0)
qc.cx(0,1)

qc.barrier()
qc.cx(0,2)
acx = XGate().control(1, ctrl_state='0')
qc.append(acx, [1,2])

cr_record = ClassicalRegister(1, name="Record Outcome")
qc.add_register(cr_record)

qc.measure(2,0)
qc.barrier()
qc.cx(0,1)

cr_qubit = ClassicalRegister(1, name="Qubit Outcome")
qc.add_register(cr_qubit)
qc.h(0)
qc.measure(0,1)



# measure


# Draw the circuit
figure = qc.draw("mpl")
figure.savefig("circuit.png")
st.image("circuit.png")

def runIBMButton():
    if st.button('Run Quantum Circuit'):
        # Execute the quantum circuit
        backend = AerSimulator()
        qc_transpiled = transpile(qc, backend)

        result = backend.run(qc_transpiled, shots=1000).result()

        figure2 = plot_histogram(result.get_counts())
        figure2.savefig("circuit2.png")
        st.image("circuit2.png")
        st.write(result.get_counts())

runIBMButton()