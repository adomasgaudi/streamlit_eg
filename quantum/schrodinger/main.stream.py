from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qr_atom = QuantumRegister(1, name="atom")
qc = QuantumCircuit(qr_atom)
qc.h(qr_atom)   
qc.draw('mpl')