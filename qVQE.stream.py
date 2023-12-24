import streamlit as st
import qiskit
import numpy as np 
import pylab
import copy
from qiskit import QuantumCircuit, BasicAer
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.aqua import aqua_globals, QuantumInstance
from qiskit.aqua.algorithms import VQE, NumPyMinimumEigensolver
from qiskit.aqua.components.optimizers import SLSQP
from qiskit.chemistry.componentst.initial_states import HartreeFock
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.drivers import PySCFDriver
from qiskit.chemistry.core import Hamiltonian, QubitMappingType



def main():
    st.title("Quantum Circuit")

    if st.button('Run Quantum Circuit'):
        molecule = 'H .0 .0 -{0}; Li .0 .0 {0}'
        distances = np.arange(0.5, 4.25, 0.25)
        vqe_energies = []
        energies = []
        exact_energies = []

        for i, d in enumerate(distances):
            print('step', i)
            # set up experiment
            driver = PySCFDriver(molecule.format(d/2), basis='sto3g')
            qmolecule = driver.run()
            operator =  Hamiltonian(
                qubit_mapping=QubitMappingType.PARITY, 
                two_qubit_reduction=True,
                freeze_core=True,
                orbital_reduction=[-3, -2]
            )
            qubit_op, aux_ops = operator.run(qmolecule)

            #exact classical result
            exact_result = NumPyMinimumEigensolver(
                qubit_op, aux_operators=aux_ops
            ).run()
            exact_result = operator.process_algorithm_result(exact_result)

            optimizer = SLSQP(maxiter=1000)
            initial_state = HartreeFock(
                operator.molecule_info['num_orbitals'],
                operator.molecule_info['num_particles'],
                qubit_mapping=operator._qubit_mapping,
                two_qubit_reduction=operator._two_qubit_reduction
            )
            var_form = UCCSD(
                num_orbitals=operator.molecule_info['num_orbitals'],
                num_particles=operator.molecule_info['num_particles'],
                initial_state=initial_state,
                qubit_mapping=operator._qubit_mapping,
                two_qubit_reduction=operator._two_qubit_reduction
            )
                             
            algo = VQE(qubit_op, var_from, optimizer, aux_operators=aux_ops)

            vqe_result = algo.run(QuantumInstance(BasicAer.get_backend('statevector_simulator')))
            vqe_result = operator.process_algorithm_result(vqe_result)

            exact_energies.append(exact_result.energy)
            vqe_energies.append(vqe_result.energy)
            hf_energies.append(vqe_result.hartree_fock_energy)


        #     quantum_instance = QuantumInstance(BasicAer.get_backend('statevector_simulator'))
        #     vqe_result = operator.process_algorithm_result(vqe_result)
        #     exact_energies.append(exact_result.energy)
        #     vqe_energies.append(vqe_result.energy)
        #     energies.append(vqe_result.energy)
        #     print("Interatomic Distance:", np.round(d, 2), "VQE Result:", vqe_result.energy, "Exact Energy:", exact_result.energy)
        # pylab.plot(distances, vqe_energies, label='VQE')
        # pylab.plot(distances, exact_energies, label='Exact')
        # pylab.plot(distances, energies, label='VQE')
        # pylab.xlabel('Atomic distance (Angstrom)')
        # pylab.ylabel('Energy (Hartree)')
        # pylab.title('LiH Ground State Energy')
        # pylab.legend(loc='upper right')
        # pylab.savefig('LiH.png')
        # pylab.show()






        # Create empty circuit
        # example_circuit = QuantumCircuit(2)
        # example_circuit.measure_all()

        # # You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
        # service = QiskitRuntimeService(channel="ibm_quantum", token="d79a58cef57641543701b758b34f4eab6b344d1d52a9e18e3d42695dc153028be326695f1388c5b276d36c4a963d1ba15be8ed096a3cfe79be3559411529758c")
        # backend = service.backend("ibmq_qasm_simulator")
        # job = Sampler(backend).run(example_circuit)
        # job_id = job.job_id()
        # st.write(f"Job ID: {job_id}")  # Display the job id
        # result = job.result()
        # st.write(result)  # Display the result

        # # Create a new circuit with two qubits (first argument) and two classical bits (second argument)
        # qc = QuantumCircuit(2)

        # # Add a Hadamard gate to qubit 0
        # qc.h(0)

        # # Perform a controlled-X gate on qubit 1, controlled by qubit 0
        # qc.cx(0, 1)

        # # Return a drawing of the circuit using MatPlotLib ("mpl"). This is the last line of the cell, so the drawing appears in the cell output.
        # # Remove the "mpl" argument to get a text drawing.
        # figure = qc.draw("mpl")
        # figure.savefig("circuit.png")

        # # Display the image
        # st.image("circuit.png")

main()