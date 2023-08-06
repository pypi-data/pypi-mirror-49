# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import unittest
import os

import numpy as np
from parameterized import parameterized

from test.common import QiskitAquaTestCase
from qiskit import BasicAer
from qiskit.aqua import Operator, run_algorithm, QuantumInstance, aqua_globals
from qiskit.aqua.input import EnergyInput
from qiskit.aqua.components.variational_forms import RY
from qiskit.aqua.components.optimizers import L_BFGS_B, COBYLA
from qiskit.aqua.components.initial_states import Zero
from qiskit.aqua.algorithms import VQE


class TestVQE(QiskitAquaTestCase):

    def setUp(self):
        super().setUp()
        np.random.seed(50)
        pauli_dict = {
            'paulis': [{"coeff": {"imag": 0.0, "real": -1.052373245772859}, "label": "II"},
                       {"coeff": {"imag": 0.0, "real": 0.39793742484318045}, "label": "IZ"},
                       {"coeff": {"imag": 0.0, "real": -0.39793742484318045}, "label": "ZI"},
                       {"coeff": {"imag": 0.0, "real": -0.01128010425623538}, "label": "ZZ"},
                       {"coeff": {"imag": 0.0, "real": 0.18093119978423156}, "label": "XX"}
                       ]
        }
        qubit_op = Operator.load_from_dict(pauli_dict)
        self.algo_input = EnergyInput(qubit_op)

    def test_vqe_via_run_algorithm(self):
        coupling_map = [[0, 1]]
        basis_gates = ['u1', 'u2', 'u3', 'cx', 'id']

        params = {
            'algorithm': {'name': 'VQE'},
            'backend': {'name': 'statevector_simulator',
                        'provider': 'qiskit.BasicAer',
                        'coupling_map': coupling_map,
                        'basis_gates': basis_gates},
        }
        result = run_algorithm(params, self.algo_input)
        self.assertAlmostEqual(result['energy'], -1.85727503)
        np.testing.assert_array_almost_equal(result['eigvals'], [-1.85727503], 5)
        ref_opt_params = [-0.58294401, -1.86141794, -1.97209632, -0.54796022,
                          -0.46945572, 2.60114794, -1.15637845,  1.40498879,
                          1.14479635, -0.48416694, -0.66608349, -1.1367579,
                          -2.67097002, 3.10214631, 3.10000313, 0.37235089]
        np.testing.assert_array_almost_equal(result['opt_params'], ref_opt_params, 5)
        self.assertIn('eval_count', result)
        self.assertIn('eval_time', result)

    @parameterized.expand([
        ['CG', 5, 4],
        ['CG', 5, 1],
        ['COBYLA', 5, 1],
        ['L_BFGS_B', 5, 4],
        ['L_BFGS_B', 5, 1],
        ['NELDER_MEAD', 5, 1],
        ['POWELL', 5, 1],
        ['SLSQP', 5, 4],
        ['SLSQP', 5, 1],
        ['SPSA', 3, 2], # max_evals_grouped=n is considered as max_evals_grouped=2 if n>2
        ['SPSA', 3, 1],
        ['TNC', 2, 4],
        ['TNC', 2, 1]
    ])
    def test_vqe_optimizers(self, name, places, max_evals_grouped):
        backend = BasicAer.get_backend('statevector_simulator')
        params = {
            'algorithm': {'name': 'VQE', 'max_evals_grouped': max_evals_grouped},
            'optimizer': {'name': name},
            'backend': {'shots': 1}
        }
        result = run_algorithm(params, self.algo_input, backend=backend)
        self.assertAlmostEqual(result['energy'], -1.85727503, places=places)

    @parameterized.expand([
        ['RY', 5],
        ['RYRZ', 5]
    ])
    def test_vqe_var_forms(self, name, places):
        backend = BasicAer.get_backend('statevector_simulator')
        params = {
            'algorithm': {'name': 'VQE'},
            'variational_form': {'name': name},
            'backend': {'shots': 1}
        }
        result = run_algorithm(params, self.algo_input, backend=backend)
        self.assertAlmostEqual(result['energy'], -1.85727503, places=places)

    @parameterized.expand([
        [4],
        [1]
    ])
    def test_vqe_direct(self, max_evals_grouped):
        backend = BasicAer.get_backend('statevector_simulator')
        num_qubits = self.algo_input.qubit_op.num_qubits
        init_state = Zero(num_qubits)
        var_form = RY(num_qubits, 3, initial_state=init_state)
        optimizer = L_BFGS_B()
        algo = VQE(self.algo_input.qubit_op, var_form, optimizer, 'paulis', max_evals_grouped=max_evals_grouped)
        quantum_instance = QuantumInstance(backend)
        result = algo.run(quantum_instance)
        self.assertAlmostEqual(result['energy'], -1.85727503)
        if quantum_instance.has_circuit_caching:
            self.assertLess(quantum_instance._circuit_cache.misses, 3)

    def test_vqe_callback(self):

        tmp_filename = 'vqe_callback_test.csv'
        is_file_exist = os.path.exists(self._get_resource_path(tmp_filename))
        if is_file_exist:
            os.remove(self._get_resource_path(tmp_filename))

        def store_intermediate_result(eval_count, parameters, mean, std):
            with open(self._get_resource_path(tmp_filename), 'a') as f:
                content = "{},{},{:.5f},{:.5f}".format(eval_count, parameters, mean, std)
                print(content, file=f, flush=True)

        backend = BasicAer.get_backend('qasm_simulator')
        num_qubits = self.algo_input.qubit_op.num_qubits
        init_state = Zero(num_qubits)
        var_form = RY(num_qubits, 1, initial_state=init_state)
        optimizer = COBYLA(maxiter=3)
        algo = VQE(self.algo_input.qubit_op, var_form, optimizer, 'paulis',
                   callback=store_intermediate_result)
        aqua_globals.random_seed = 50
        quantum_instance = QuantumInstance(backend, seed_transpiler=50, shots=1024, seed=50)
        algo.run(quantum_instance)

        is_file_exist = os.path.exists(self._get_resource_path(tmp_filename))
        self.assertTrue(is_file_exist, "Does not store content successfully.")

        # check the content
        ref_content = [['1', '[-0.03391886 -1.70850424 -1.53640265 -0.65137839]', '-0.61121', '0.01572'],
                       ['2', '[ 0.96608114 -1.70850424 -1.53640265 -0.65137839]', '-0.79235', '0.01722'],
                       ['3', '[ 0.96608114 -0.70850424 -1.53640265 -0.65137839]', '-0.82829', '0.01529']
                       ]
        try:
            with open(self._get_resource_path(tmp_filename)) as f:
                idx = 0
                for record in f.readlines():
                    eval_count, parameters, mean, std = record.split(",")
                    self.assertEqual(eval_count.strip(), ref_content[idx][0])
                    self.assertEqual(parameters, ref_content[idx][1])
                    self.assertEqual(mean.strip(), ref_content[idx][2])
                    self.assertEqual(std.strip(), ref_content[idx][3])
                    idx += 1
        finally:
            if is_file_exist:
                os.remove(self._get_resource_path(tmp_filename))


if __name__ == '__main__':
    unittest.main()
