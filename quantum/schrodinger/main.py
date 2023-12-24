from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qr_atom = QuantumRegister(1, name="atom")
qc = QuantumCircuit(qr_atom)
qc.h(qr_atom)   
qc.draw('mpl')

backend = AerSimulator()

qr_cat = QuantumRegister(1, name="cat")
qc = QuantumCircuit(qr_atom, qr_cat)
qc.h(qr_atom[0])
qc.cx(qr_atom[0], qr_cat[0])
qr_observer = QuantumRegister(1, name="observer")
qc = QuantumCircuit(qr_atom, qr_cat, qr_observer)
qc.h(qr_atom[0])
qc.cx(qr_atom[0], qr_cat[0])
qc.cx(qr_cat[0], qr_observer[0])

qc.measure_all()
result = backend.run(qc, shots=1000).result()
print(result.get_counts())
qc.draw('mpl')