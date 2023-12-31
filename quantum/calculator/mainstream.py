import streamlit as st
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram

# Streamlit Title
st.title("Quantum 2-Bit Binary Adder")

# Function to create a 2-bit binary adder circuit
def create_2bit_adder_circuit(a0, a1, b0, b1):
    tba = QuantumCircuit(11, 3)

    # Step 1: Encode input
    if a0: tba.x(0) # LSB of first number
    if a1: tba.x(1) # MSB of first number
    if b0: tba.x(2) # LSB of second number
    if b1: tba.x(3) # MSB of second number

    tba.barrier()

    # Step 2: Operations
    # Adding 2^0 bit
    tba.cx(0, 4)
    tba.cx(2, 4)

    tba.barrier()

    # Adding 2^1 bit
    tba.ccx(0, 2, 5)
    tba.cx(1, 6)
    tba.cx(3, 6)
    tba.cx(5, 7)
    tba.cx(6, 7)

    tba.barrier()

    # Adding 2^2 bit
    tba.ccx(5, 6, 8)
    tba.ccx(1, 3, 9)

    tba.barrier()

    # Constructing OR gate for 2^2 bit
    tba.x(8)
    tba.x(9)
    tba.ccx(8, 9, 10)
    tba.x(10)

    tba.barrier()

    # Step 3: Extract output
    tba.measure(4, 0)  # LSB Sum
    tba.measure(7, 1)  # MSB Sum
    tba.measure(10, 2) # Carry

    return tba

# Input checkboxes for each bit of the two numbers
a0 = st.checkbox("Input A0 (1st number, LSB)")
a1 = st.checkbox("Input A1 (1st number, MSB)")
b0 = st.checkbox("Input B0 (2nd number, LSB)")
b1 = st.checkbox("Input B1 (2nd number, MSB)")

# Create and display the quantum circuit
qc = create_2bit_adder_circuit(a0, a1, b0, b1)
st.pyplot(qc.draw(output='mpl'))

# Button to run the quantum circuit
if st.button('Calculate Sum'):
    backend = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, backend)
    result = backend.run(transpiled_qc, shots=1024).result()
    counts = result.get_counts()

    # Display the histogram of results
    st.pyplot(plot_histogram(counts))
    st.write("Result Counts:", counts)

    # Convert the binary results to decimal
    decimal_results = {int(k, 2): v for k, v in counts.items()}

    # Display the decimal results
    st.write("Decimal Results:", decimal_results)

    # Display the addition formula
    a_decimal = a1 * 2 + a0
    b_decimal = b1 * 2 + b0
    st.write(f"{a_decimal} + {b_decimal} = {max(decimal_results.keys())} ({bin(max(decimal_results.keys()))[2:].zfill(3)})")
