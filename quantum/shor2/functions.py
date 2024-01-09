from utils import *
from qiskit import QuantumCircuit

def c_amod15(var_a, power):
    st.write(f"Controlled multiplication by {var_a} mod 15, power {power}")
    
    U = QuantumCircuit(4)
    for _ in range(power):
        U.swap(0,1)
        U.swap(1,2)
        U.swap(2,3)
        for q in range(4):
            U.x(q)

    if power < 4:
        create_photo(U)

    U = U.to_gate()
    U.name = f"{var_a}^{power} mod 15"
    c_U = U.control()
    return c_U

