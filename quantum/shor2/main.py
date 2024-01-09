import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT
from math import gcd
from fractions import Fraction
import streamlit as st
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from random import randint
from math import gcd # greatest common divisor
import streamlit as st
from utils import create_photo
from functions import c_amod15

MY_TOKEN = 'd79a58cef57641543701b758b34f4eab6b344d1d52a9e18e3d42695dc153028be326695f1388c5b276d36c4a963d1ba15be8ed096a3cfe79be3559411529758c'




#/ .----------------.  .----------------.  .----------------. 
#| .--------------. || .--------------. || .--------------. |
#| |              | || |              | || |              | |
#| |              | || |              | || |              | |
#| |    ______    | || |    ______    | || |    ______    | |
#| |   |______|   | || |   |______|   | || |   |______|   | |
#| |              | || |              | || |              | |
#| |              | || |              | || |              | |
#| |              | || |              | || |              | |
#| '--------------' || '--------------' || '--------------' |
# '----------------'  '----------------'  '----------------' 




st.title('Shors Algorithm')
st.write('Probably the most famous, practical and feasable aplication of a quantum computer would be to find the prime factors of large numbers. This is a task that gets exponentially more difficult with larger numbers, while classical computer can only get geometrically more powerful. Hence a large enough number will be impractical for a classical computer to solve. This is a computational complexity phenomenon that is exploited to create cryptographic keys. However, a quantum computer could solve this problem in polynomial time. This is the basis of Shor’s algorithm, which is one of the most famous quantum algorithms. Shor’s algorithm is a quantum algorithm for integer factorization. It was published in 1994 by the American mathematician Peter Shor. It solves the following problem: Given an integer N, find its prime factors. On a quantum computer, to factor an integer N, Shor’s algorithm runs in polynomial time (the time taken is polynomial in log N, which is the size of the input).')


N = 15

np.random.seed(1) # For reproduceable results
VAR_A = randint(2, 15)
st.write(VAR_A)
gcd(VAR_A, N)

st.write(f"Greatest common divisor: {gcd(VAR_A, N)}")

st.video('https://www.youtube.com/watch?v=lvTqbM5Dq4Q')
# Specify variables
N_COUNT = 8  # number of counting qubits
VAR_A = 7

def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

# Create QuantumCircuit with N_COUNT counting qubits
# plus 4 qubits for U to act on
qc = QuantumCircuit(N_COUNT + 4, N_COUNT)

# Initialize counting qubits
# in state |+>
for q in range(N_COUNT):
    qc.h(q)

# And auxiliary register in state |1>
qc.x(N_COUNT)

# Do controlled-U operations
for q in range(N_COUNT):
    st.write(f"c_amod15({VAR_A}  ,  2^{q})")
    qc.append(c_amod15(VAR_A, 2**q),
             [q] + [i+N_COUNT for i in range(4)])

# Do inverse-QFT
qc.append(qft_dagger(N_COUNT), range(N_COUNT))

# Measure circuit
qc.measure(range(N_COUNT), range(N_COUNT))
qc.draw(fold=-1)  # -1 means 'do not fold'


aer_sim = Aer.get_backend('aer_simulator')
t_qc = transpile(qc, aer_sim)
counts = aer_sim.run(t_qc).result().get_counts()
plot_histogram(counts)



rows, measured_phases = [], []
for output in counts:
    decimal = int(output, 2)  # Convert (base 2) string to decimal
    phase = decimal/(2**N_COUNT)  # Find corresponding eigenvalue
    measured_phases.append(phase)
    # Add these values to the rows in our table:
    rows.append([f"{output}(bin) = {decimal:>3}(dec)",
                 f"{decimal}/{2**N_COUNT} = {phase:.2f}"])
# Print the rows in a table
headers=["Register Output", "Phase"]
df = pd.DataFrame(rows, columns=headers)
print(df)


Fraction(0.666)

# Get fraction that most closely resembles 0.666
# with denominator < 15
Fraction(0.666).limit_denominator(15)


rows = []
for phase in measured_phases:
    frac = Fraction(phase).limit_denominator(15)
    rows.append([phase,
                 f"{frac.numerator}/{frac.denominator}",
                 frac.denominator])
# Print as a table
headers=["Phase", "Fraction", "Guess for r"]
df = pd.DataFrame(rows, columns=headers)
print(df)
st.write(df)

def a2jmodN(a, j, N):
    """Compute a^{2^j} (mod N) by repeated squaring"""
    for _ in range(j):
        a = np.mod(a**2, N)
    return a


a2jmodN(7, 2049, 53)

def qpe_amod15(a):
    """Performs quantum phase estimation on the operation a*r mod 15.
    Args:
        a (int): This is 'a' in a*r mod 15
    Returns:
        float: Estimate of the phase
    """
    N_COUNT = 8
    qc = QuantumCircuit(4+N_COUNT, N_COUNT)
    for q in range(N_COUNT):
        qc.h(q)     # Initialize counting qubits in state |+>
    qc.x(N_COUNT) # And auxiliary register in state |1>
    for q in range(N_COUNT): # Do controlled-U operations
        qc.append(c_amod15(a, 2**q),
                 [q] + [i+N_COUNT for i in range(4)])
    qc.append(qft_dagger(N_COUNT), range(N_COUNT)) # Do inverse-QFT
    qc.measure(range(N_COUNT), range(N_COUNT))
    # Simulate Results
    aer_sim = Aer.get_backend('aer_simulator')
    # `memory=True` tells the backend to save each measurement in a list
    job = aer_sim.run(transpile(qc, aer_sim), shots=1, memory=True)
    readings = job.result().get_memory()
    print("Register Reading: " + readings[0])
    st.write("Register Reading: " + readings[0])
    phase = int(readings[0],2)/(2**N_COUNT)
    print(f"Corresponding Phase: {phase}")
    st.write(f"Corresponding Phase: {phase}")
    return phase

phase = qpe_amod15(VAR_A) # Phase = s/r
print(f"Corresponding Phase: {phase}")
st.write(f"Corresponding Phase: {phase}")
Fraction(phase).limit_denominator(15)

frac = Fraction(phase).limit_denominator(15)
s, r = frac.numerator, frac.denominator
print(r)
st.write(r)

guesses = [gcd(VAR_A**(r//2)-1, N), gcd(VAR_A**(r//2)+1, N)]
print(guesses)
st.write(guesses)

VAR_A = 7
FACTOR_FOUND = False
ATTEMPT = 0
while not FACTOR_FOUND:
    ATTEMPT += 1
    print(f"\nATTEMPT {ATTEMPT}:")
    st.write(f"\nATTEMPT {ATTEMPT}:")
    phase = qpe_amod15(VAR_A) # Phase = s/r
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    print(f"Result: r = {r}")
    st.write(f"Result: r = {r}")
    if phase != 0:
        # Guesses for factors are gcd(x^{r/2} ±1 , 15)
        guesses = [gcd(VAR_A**(r//2)-1, N), gcd(VAR_A**(r//2)+1, N)]
        print(f"Guessed Factors: {guesses[0]} and {guesses[1]}")
        st.write(f"Guessed Factors: {guesses[0]} and {guesses[1]}")
        for guess in guesses:
            if guess not in [1,N] and (N % guess) == 0:
                # Guess is a factor!
                print(f"*** Non-trivial factor found: {guess} ***")
                st.write(f"*** Non-trivial factor found: {guess} ***")
                FACTOR_FOUND = True

# The cell below repeats the algorithm until at least one factor of 15
# is found
assert (3 in guesses) or (5 in guesses)