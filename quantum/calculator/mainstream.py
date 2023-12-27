import streamlit as st
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, transpile
from qiskit.visualization import plot_histogram

# Streamlit Title
st.title("Quantum 2-Bit Binary Adder")

# Function to create a full adder circuit
def full_adder(qc, a, b, c, s, carry_out):
    qc.ccx(a, b, carry_out)
    qc.cx(a, b)
    qc.ccx(c, b, carry_out)
    qc.cx(c, b)
    qc.cx(a, b)
    qc.measure([carry_out, b], [s, s+1])  # reversed order of measurements

# Quantum circuit for a 2-bit adder
def create_2bit_adder_circuit(a0, a1, b0, b1):
    # Quantum Registers: 6 qubits
    # qr = QuantumRegister(6, name="q")
    qr0 = QuantumRegister(1, name="a0")
    qr1 = QuantumRegister(1, name="a1")
    qr2 = QuantumRegister(1, name="b0")
    qr3 = QuantumRegister(1, name="b1")
    qr4 = QuantumRegister(1, name="carry_in")
    qr5 = QuantumRegister(1, name="carry_out")

    cr = ClassicalRegister(3, name="output")

    # Quantum Circuit
    qc = QuantumCircuit(qr0, qr1, qr2, qr3, qr4, qr5, cr)
    # Classical Registers: 3 bits for output (2 sum bits + 1 carry)
    # cr = ClassicalRegister(3, name="output")
    # qc = QuantumCircuit(qr, cr)

    # Setting up the input states
    if a0 == 1: qc.x(qr0[0]) # LSB of first number
    if a1 == 1: qc.x(qr1[0]) # MSB of first number
    if b0 == 1: qc.x(qr2[0]) # LSB of second number
    if b1 == 1: qc.x(qr3[0]) # MSB of second number

    # First full adder (least significant bits)
    full_adder(qc, qr0[0], qr2[0], qr4[0], 0, qr5[0]) # qr4[0] is carry-in (initially 0)

    # Second full adder (most significant bits)
    full_adder(qc, qr1[0], qr3[0], qr5[0], 1, qr4[0]) # qr5[0] is carry-out from first adder

    return qc

# Input checkboxes for each bit of the two numbers
a0 = st.checkbox("Input A0 (1st number, LSB)")
a1 = st.checkbox("Input A1 (1st number, MSB)")
b0 = st.checkbox("Input B0 (2nd number, LSB)")
b1 = st.checkbox("Input B1 (2nd number, MSB)")

# Create and display the quantum circuit
qc = create_2bit_adder_circuit(a0, a1, b0, b1)
st.pyplot(qc.draw(output='mpl'))

# Button to run the quantum circuit
# ... rest of your code ...

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
