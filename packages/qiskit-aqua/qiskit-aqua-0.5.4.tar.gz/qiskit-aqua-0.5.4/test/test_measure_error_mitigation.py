# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import unittest
import time

from qiskit import Aer
import numpy as np

from test.common import QiskitAquaTestCase
from qiskit.aqua.components.oracles import LogicalExpressionOracle
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.ignis.mitigation.measurement import CompleteMeasFitter
from qiskit.providers.aer import noise
from qiskit.aqua.algorithms import Grover


class TestMeasurementErrorMitigation(QiskitAquaTestCase):
    """Test measurement error mitigation."""

    def test_measurement_error_mitigation(self):
        aqua_globals.random_seed = 0

        # build noise model
        noise_model = noise.NoiseModel()
        read_err = noise.errors.readout_error.ReadoutError([[0.9, 0.1], [0.25, 0.75]])
        noise_model.add_all_qubit_readout_error(read_err)

        backend = Aer.get_backend('qasm_simulator')
        quantum_instance = QuantumInstance(backend=backend, seed=167, seed_transpiler=167,
                                           noise_model=noise_model)

        quantum_instance_with_mitigation = QuantumInstance(backend=backend, seed=167, seed_transpiler=167,
                                                           noise_model=noise_model,
                                                           measurement_error_mitigation_cls=CompleteMeasFitter)

        input = 'a & b & c'
        oracle = LogicalExpressionOracle(input, optimization='off')
        grover = Grover(oracle)

        result_wo_mitigation = grover.run(quantum_instance)
        prob_top_measurement_wo_mitigation = result_wo_mitigation['measurement'][
            result_wo_mitigation['top_measurement']]

        result_w_mitigation = grover.run(quantum_instance_with_mitigation)
        prob_top_measurement_w_mitigation = result_w_mitigation['measurement'][result_w_mitigation['top_measurement']]

        self.assertGreaterEqual(prob_top_measurement_w_mitigation, prob_top_measurement_wo_mitigation)

    def test_measurement_error_mitigation_auto_refresh(self):
        aqua_globals.random_seed = 0

        # build noise model
        noise_model = noise.NoiseModel()
        read_err = noise.errors.readout_error.ReadoutError([[0.9, 0.1], [0.25, 0.75]])
        noise_model.add_all_qubit_readout_error(read_err)

        backend = Aer.get_backend('qasm_simulator')
        quantum_instance = QuantumInstance(backend=backend, seed=1679, seed_transpiler=167,
                                           noise_model=noise_model,
                                           measurement_error_mitigation_cls=CompleteMeasFitter,
                                           cals_matrix_refresh_period=0)
        input = 'a & b & c'
        oracle = LogicalExpressionOracle(input, optimization='off')
        grover = Grover(oracle)
        _ = grover.run(quantum_instance)
        cals_matrix_1 = quantum_instance.cals_matrix.copy()

        time.sleep(15)
        aqua_globals.random_seed = 2
        quantum_instance.set_config(seed=111)
        _ = grover.run(quantum_instance)
        cals_matrix_2 = quantum_instance.cals_matrix.copy()

        diff = cals_matrix_1 - cals_matrix_2
        total_diff = np.sum(np.abs(diff))

        self.assertGreater(total_diff, 0.0)


if __name__ == '__main__':
    unittest.main()
