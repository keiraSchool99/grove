"""Module containing implementations of oracle Programs.
"""

import numpy as np
import pyquil.quil as pq
from pyquil.gates import X, Z

from grove.alpha.utility_programs import ControlledProgramBuilder


def basis_selector_oracle(qubits, bitstring):
    """Defines an oracle that selects the ith element of the computational basis.

    Flips the sign of the state :math:`\\vert x\\rangle>`
    if and only if x==bitstring and does nothing otherwise.

    :param qubits: The qubits the oracle is called on. The qubits are assumed to be ordered from
     most significant qubit to least significant qubit.
    :param bitstring: The desired bitstring, given as a string of ones and zeros. e.g. "101"
    :return: A program representing this oracle.
    :rtype: Program
    """
    if len(qubits) != len(bitstring):
        raise ValueError(
            "The bitstring should be the same length as the number of qubits.")
    oracle_prog = pq.Program()

    # In the case of one qubit, we just want to flip the phase of state relative to the other.
    if len(bitstring) == 1:
        oracle_prog.inst(Z(qubits[0]))
        return oracle_prog
    else:
        for i, qubit in enumerate(qubits):
            if bitstring[i] == '0':
                oracle_prog.inst(X(qubit))
        controls = qubits[:-1]
        target = qubits[-1]
        operation = np.array([[1, 0], [0, -1]])
        gate_name = 'Z'
        n_qubit_controlled_z = ControlledProgramBuilder().with_controls(controls).with_target(
            target).with_operation(operation).with_gate_name(gate_name).build()

        oracle_prog += n_qubit_controlled_z

        for i, qubit in enumerate(qubits):
            if bitstring[i] == '0':
                oracle_prog.inst(X(qubit))
    return oracle_prog
