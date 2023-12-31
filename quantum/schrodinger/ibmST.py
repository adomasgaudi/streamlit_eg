import streamlit as st
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

MY_TOKEN = 'd79a58cef57641543701b758b34f4eab6b344d1d52a9e18e3d42695dc153028be326695f1388c5b276d36c4a963d1ba15be8ed096a3cfe79be3559411529758c'

st.title("Schrodinger's Cat")
st.title("Quantum Circuit")

 
# Save an IBM Quantum account and set it as your default account.
QiskitRuntimeService.save_account(channel="ibm_quantum", token=MY_TOKEN , set_as_default=True, overwrite=True)


 
# Load saved credentials
service = QiskitRuntimeService()
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
        # # Execute the quantum circuit
        # backend = AerSimulator()
        # result = backend.run(qc, shots=100).result()
        # st.write(result.get_counts())
        # ibmq_qasm_simulator
        service = QiskitRuntimeService()
        backend = service.backend("ibmq_qasm_simulator")
        job = Sampler(backend).run(qc)
        st.write(f"job id: {job.job_id()}")
        result = job.result()
        counts = result.quasi_dists[0]
        # Convert the keys from decimal to binary
        counts2 = {format(key, '03b'): value for key, value in result.quasi_dists[0].items()}
        st.write(counts2)
        st.write(counts)
        print(result)
        st.write(result)
runIBMButton()