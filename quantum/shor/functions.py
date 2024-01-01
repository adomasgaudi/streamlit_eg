from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import streamlit as st
import pandas as pd 


MY_TOKEN = 'd79a58cef57641543701b758b34f4eab6b344d1d52a9e18e3d42695dc153028be326695f1388c5b276d36c4a963d1ba15be8ed096a3cfe79be3559411529758c'

def create_controlled_amod15_circuit(a, power):
    """Create a controlled circuit for multiplication by a mod 15."""
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13")
    U = QuantumCircuit(4)
    for _ in range(power):
        if a in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    return U.control()


def create_quantum_fourier_transform_circuit(n):
    """Create an n-qubit Quantum Fourier Transform circuit."""
    qc = QuantumCircuit(n)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2**(j-m)), m, j)
        qc.h(j)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    qc.name = "QFT†"
    return qc

def setup_shors_algorithm_circuit(n_count, a):
    """Setup the quantum circuit for Shor's Algorithm."""
    qc = QuantumCircuit(n_count + 4, n_count)
    # Initialize counting qubits in state |+>
    for q in range(n_count):
        qc.h(q)
    # And auxiliary register in state |1>
    qc.x(n_count + 3)
    # Do controlled-U operations
    for q in range(n_count):
        qc.append(create_controlled_amod15_circuit(a, 2**q), [q] + [i+n_count for i in range(4)])
    # Do inverse-QFT
    qc.append(create_quantum_fourier_transform_circuit(n_count), range(n_count))
    # Measure circuit
    qc.measure(range(n_count), range(n_count))
    return qc


def run_quantum_circuit(qc, n_count):
    """Run the quantum circuit on IBM Quantum simulator and display results."""
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=MY_TOKEN, set_as_default=True, overwrite=True)
    service = QiskitRuntimeService()

    t_qc = transpile(qc, service.backend("ibmq_qasm_simulator"))
    sampler = Sampler(service.backend("ibmq_qasm_simulator"))
    job = sampler.run(t_qc)
    result = job.result()

    counts = result.quasi_dists[0]
    process_and_display_results(counts, n_count)

def process_and_display_results(counts, n_count):
    """Process and display the results of the quantum circuit."""
    rows, measured_phases = [], []
    for output in counts:
        decimal = int(output, 2)  # Convert (base 2) string to decimal
        phase = decimal / (2**n_count)  # Find corresponding eigenvalue
        measured_phases.append(phase)
        rows.append([f"{output}(bin) = {decimal:>3}(dec)", f"{decimal}/{2**n_count} = {phase:.2f}"])

    headers = ["Register Output", "Phase"]
    df = pd.DataFrame(rows, columns=headers)
    st.write(df)

    plot_and_save_histogram(counts)

def plot_and_save_histogram(counts):
    """Plot and save the histogram of the quantum circuit results."""
    # fig = plot_histogram(counts)
    plt.savefig("histogram.png")
    st.image("histogram.png")


