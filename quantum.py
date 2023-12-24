import streamlit as st
import qiskit
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

def main():
    st.title("Quantum Circuit")

    if st.button('Run Quantum Circuit'):
        # Create empty circuit
        example_circuit = QuantumCircuit(2)
        example_circuit.measure_all()

        # You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
        service = QiskitRuntimeService(channel="ibm_quantum", token="d79a58cef57641543701b758b34f4eab6b344d1d52a9e18e3d42695dc153028be326695f1388c5b276d36c4a963d1ba15be8ed096a3cfe79be3559411529758c")
        backend = service.backend("ibmq_qasm_simulator")
        job = Sampler(backend).run(example_circuit)
        job_id = job.job_id()
        st.write(f"Job ID: {job_id}")  # Display the job id
        result = job.result()
        st.write(result)  # Display the result

        # Create a new circuit with two qubits (first argument) and two classical bits (second argument)
        qc = QuantumCircuit(2)

        # Add a Hadamard gate to qubit 0
        qc.h(0)

        # Perform a controlled-X gate on qubit 1, controlled by qubit 0
        qc.cx(0, 1)

        # Return a drawing of the circuit using MatPlotLib ("mpl"). This is the last line of the cell, so the drawing appears in the cell output.
        # Remove the "mpl" argument to get a text drawing.
        figure = qc.draw("mpl")
        figure.savefig("circuit.png")

        # Display the image
        st.image("circuit.png")

main()