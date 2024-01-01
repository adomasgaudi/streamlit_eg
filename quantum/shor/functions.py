
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
        # ... (rest of the logic)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    return U.control()

def create_quantum_fourier_transform_circuit(n):
    """Create an n-qubit Quantum Fourier Transform circuit."""
    qc = QuantumCircuit(n)
    # Logic for Quantum Fourier Transform
    # ... (rest of the logic)
    qc.name = "QFT†"
    return qc

def setup_shors_algorithm_circuit(n_count, a):
    """Setup the quantum circuit for Shor's Algorithm."""
    qc = QuantumCircuit(n_count + 4, n_count)
    # Initialize qubits and perform controlled-U operations
    # ... (rest of the logic)
    return qc

def run_quantum_circuit(qc):
    """Run the quantum circuit on IBM Quantum simulator and display results."""
    # Save an IBM Quantum account and set it as the default account
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=MY_TOKEN, set_as_default=True, overwrite=True)
    service = QiskitRuntimeService()

    # Transpile and run the circuit
    t_qc = transpile(qc, service.backend("ibmq_qasm_simulator"))
    sampler = Sampler(service.backend("ibmq_qasm_simulator"))
    job = sampler.run(t_qc)
    result = job.result()

    # Process and display results
    counts = result.quasi_dists[0]
    binary_counts = {format(key, '03b'): value for key, value in counts.items()}
    st.write("Resulting Counts:", binary_counts)
    plot_and_save_histogram(binary_counts)

def plot_and_save_histogram(counts):
    """Plot and save the histogram of the quantum circuit results."""
    fig = plot_histogram(counts)
    plt.savefig("histogram.png")
    st.image("histogram.png")