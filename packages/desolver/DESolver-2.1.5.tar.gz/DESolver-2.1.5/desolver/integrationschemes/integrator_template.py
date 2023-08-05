"""
The MIT License (MIT)

Copyright (c) 2019 Microno95, Ekin Ozturk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy
import numpy.linalg

from .. import utilities as deutil

class IntegratorTemplate(object):
    def __init__(self):
        raise NotImplementedError("Do not initialise this class directly!")

    def forward(self):
        raise NotImplementedError("Do not use this class directly! How did you initialise it??")

    __call__ = forward

    def get_aux_array(self, current_state):
        return numpy.stack([numpy.zeros_like(current_state) for i in range(self.num_stages)])

class ExplicitIntegrator(IntegratorTemplate):
    tableau = None
    final_state = None
    __symplectic__ = False

    def __init__(self, sys_dim, rtol=None, atol=None):
        self.dim = sys_dim
        self.rtol=rtol
        self.atol=atol
        self.adaptive = numpy.shape(self.final_state)[0] == 2
        self.num_stages = numpy.shape(self.tableau)[0]

    def forward(self, rhs, initial_time, initial_state, constants, timestep):
        nfev = 0
        if self.tableau is None:
            raise NotImplementedError("In order to use the fixed step integrator, subclass this class and populate the butcher tableau")
        else:
            aux = self.get_aux_array(initial_state)

            for stage in range(self.num_stages):
                current_time  = initial_time  + self.tableau[stage, 0]*timestep
                current_state = initial_state + numpy.einsum("n,n...->...", self.tableau[stage, 1:], aux)
                aux[stage] = rhs(current_time, current_state, **constants) * timestep
                nfev += 1

            final_time  = initial_time  + timestep
            dState      = numpy.einsum("n,n...->...", self.final_state[0, 1:], aux)
            final_state = initial_state + numpy.einsum("n,n...->...", self.final_state[0, 1:], aux)
            nfev2 = 0
            if self.adaptive:
                final_state2 = initial_state + numpy.einsum("n,n...->...", self.final_state[1, 1:], aux)
                timestep, redo_step = self.update_timestep(final_state, final_state2, initial_time, timestep)
                if redo_step:
                    timestep, (final_time, final_state, dState), nfev2 = self(rhs, initial_time, initial_state, constants, timestep)
            return timestep, (final_time, final_state, dState), nfev + nfev2

    __call__ = forward

    def update_timestep(self, final_state1, final_state2, initial_time, timestep, tol=0.9):
        err_estimate = numpy.abs(final_state1 - final_state2).max()
        relerr = self.atol + self.rtol * err_estimate
        if err_estimate != 0:
            corr = timestep * tol * (relerr / err_estimate) ** (1.0 / self.num_stages)
            if corr != 0:
                timestep = corr
        if err_estimate > relerr:
            return timestep, True
        else:
            return timestep, False

class SymplecticIntegrator(IntegratorTemplate):
    tableau = None
    __symplectic__ = True

    def __init__(self, sys_dim, staggered_mask=None, rtol=None, atol=None):
        if staggered_mask is None:
            staggered_mask = numpy.arange(sys_dim[0]//2, sys_dim[0])
            self.staggered_mask = numpy.zeros(sys_dim, dtype=numpy.bool)
            self.staggered_mask[staggered_mask] = True
        else:
            self.staggered_mask = staggered_mask.astype(numpy.bool)

        self.dim = sys_dim
        self.rtol=rtol
        self.atol=atol
        self.adaptive = False
        self.num_stages = numpy.shape(self.tableau)[0]

    def get_aux_array(self, current_state):
        return numpy.zeros_like(current_state)

    def forward(self, rhs, initial_time, initial_state, constants, timestep):
        nfev = 0
        if self.tableau is None:
            raise NotImplementedError("In order to use the fixed step integrator, subclass this class and populate the butcher tableau")
        else:
            msk = self.staggered_mask
            nmsk = numpy.logical_not(self.staggered_mask)

            current_time = numpy.copy(initial_time)
            current_state = numpy.copy(initial_state)
            dState = numpy.zeros_like(current_state)

            # print(msk, nmsk)
            
            for stage in range(self.num_stages):
                aux = self.get_aux_array(initial_state)
                aux = rhs(current_time, current_state, **constants) * timestep
                current_time        += timestep  * self.tableau[stage, 0]
                current_state[nmsk] += aux[nmsk] * self.tableau[stage, 1]
                current_state[msk]  += aux[msk]  * self.tableau[stage, 2]
                dState[nmsk]        += aux[nmsk] * self.tableau[stage, 1]
                dState[msk]         += aux[msk]  * self.tableau[stage, 2]
                nfev += 1
                
            final_time  = current_time
            final_state = current_state
            return timestep, (final_time, final_state, dState), nfev

    __call__ = forward

    def update_timestep(self, final_state1, final_state2, initial_time, timestep, tol=0.9):
        err_estimate = numpy.abs(final_state1 - final_state2).max()
        relerr = self.atol + self.rtol * err_estimate
        if err_estimate != 0:
            corr = timestep * tol * (relerr / err_estimate) ** (1.0 / self.num_stages)
            if corr != 0:
                timestep = corr
        if err_estimate > relerr:
            return timestep, True
        else:
            return timestep, False
