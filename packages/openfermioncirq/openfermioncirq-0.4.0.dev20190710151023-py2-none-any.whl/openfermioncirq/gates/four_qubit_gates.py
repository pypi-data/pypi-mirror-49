# coding=utf-8
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

u"""Gates that target four qubits."""


from __future__ import division
from __future__ import absolute_import
from typing import Optional, Union, Tuple

import numpy as np
import sympy

import cirq
from cirq._compat import proper_repr


class DoubleExcitationGate(cirq.EigenGate):
    u"""Evolve under -|0011><1100| + h.c. for some time."""

    def __init__(self, **_3to2kwargs):
        if 'duration' in _3to2kwargs: duration = _3to2kwargs['duration']; del _3to2kwargs['duration']
        else: duration = None
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs = None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads = None
        if 'exponent' in _3to2kwargs: exponent = _3to2kwargs['exponent']; del _3to2kwargs['exponent']
        else: exponent = None
        u"""Initialize the gate.

        At most one of exponent, rads, degs, or duration may be specified.
        If more are specified, the result is considered ambiguous and an
        error is thrown. If no argument is given, the default value of one
        half-turn is used.

        Args:
            exponent: The exponent angle, in half-turns.
            rads: The exponent angle, in radians.
            degs: The exponent angle, in degrees.
            duration: The exponent as a duration of time.
        """

        if len([1 for e in [exponent, rads, degs, duration]
                if e is not None]) > 1:
            raise ValueError(u'Redundant exponent specification. '
                             u'Use ONE of exponent, rads, degs, or duration.')

        if duration is not None:
            exponent = 2 * duration / np.pi
        else:
            exponent = cirq.chosen_angle_to_half_turns(
                half_turns=exponent,
                rads=rads,
                degs=degs)

        super(DoubleExcitationGate, self).__init__(exponent=exponent)

    def num_qubits(self):
        return 4

    def _eigen_components(self):
        minus_one_component = np.zeros((16, 16))
        minus_one_component[3, 3] = minus_one_component[12, 12] = 0.5
        minus_one_component[3, 12] = minus_one_component[12, 3] = -0.5

        plus_one_component = np.zeros((16, 16))
        plus_one_component[3, 3] = plus_one_component[12, 12] = 0.5
        plus_one_component[3, 12] = plus_one_component[12, 3] = 0.5

        return [(0, np.diag([1, 1, 1, 0, 1, 1, 1, 1,
                             1, 1, 1, 1, 0, 1, 1, 1])),
                (-1, minus_one_component),
                (1, plus_one_component)]

    def _apply_unitary_(self, args
                        ):
        if cirq.is_parameterized(self):
            return None
        inner_matrix = cirq.unitary(cirq.Rx(-2 * np.pi * self.exponent))
        a = args.subspace_index(0b0011)
        b = args.subspace_index(0b1100)
        return cirq.apply_matrix_to_slices(args.target_tensor,
                                           inner_matrix,
                                           slices=[a, b],
                                           out=args.available_buffer)

    def _with_exponent(self,
                       exponent
                       ):
        return DoubleExcitationGate(exponent=exponent)

    def _decompose_(self, qubits):
        p, q, r, s = qubits

        rq_phase_block = [cirq.Z(q) ** 0.125,
                          cirq.CNOT(r, q),
                          cirq.Z(q) ** -0.125]

        srq_parity_transform = [cirq.CNOT(s, r),
                                cirq.CNOT(r, q),
                                cirq.CNOT(s, r)]

        phase_parity_block = [[rq_phase_block,
                              srq_parity_transform,
                              rq_phase_block]]

        yield cirq.CNOT(r, s)
        yield cirq.CNOT(q, p)
        yield cirq.CNOT(q, r)
        yield cirq.X(q) ** -self.exponent
        yield phase_parity_block

        yield cirq.CNOT(p, q)
        yield cirq.X(q)
        yield phase_parity_block
        yield cirq.X(q) ** self.exponent
        yield phase_parity_block
        yield cirq.CNOT(p, q)
        yield cirq.X(q)

        yield phase_parity_block
        yield cirq.CNOT(q, p)
        yield cirq.CNOT(q, r)
        yield cirq.CNOT(r, s)

    def _circuit_diagram_info_(self, args
                               ):
        if args.use_unicode_characters:
            wire_symbols = (u'⇅', u'⇅', u'⇵', u'⇵')
        else:
            wire_symbols = (ur'/\ \/',
                            ur'/\ \/',
                            u'\/ /\\',
                            u'\/ /\\')
        return cirq.CircuitDiagramInfo(
            wire_symbols=wire_symbols,
            exponent=self._diagram_exponent(args))

    def __repr__(self):
        if self.exponent == 1:
            return u'ofc.DoubleExcitation'
        return u'(ofc.DoubleExcitation**{})'.format(proper_repr(self.exponent))


DoubleExcitation = DoubleExcitationGate()
