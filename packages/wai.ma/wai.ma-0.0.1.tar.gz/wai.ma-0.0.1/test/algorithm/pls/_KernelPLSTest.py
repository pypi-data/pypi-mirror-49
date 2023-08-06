#  _KernelPLSTest.py
#  Copyright (C) 2019 University of Waikato, Hamilton, New Zealand
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from ._AbstractPLSTest import AbstractPLSTest
from ...test.misc import TestRegression
from wai.ma.algorithm.pls import KernelPLS
from wai.ma.transformation.kernel import LinearKernel, PolyKernel, RBFKernel


class KernelPLSTest(AbstractPLSTest[KernelPLS]):
    """
    Test case for the KernelPLS algorithm.
    """
    @TestRegression
    def linear_kernel(self):
        self.subject.kernel = LinearKernel()

    @TestRegression
    def poly_kernel(self):
        self.subject.kernel = PolyKernel()

    @TestRegression
    def rbf_kernel(self):
        self.subject.kernel = RBFKernel()

    def instantiate_subject(self) -> KernelPLS:
        return KernelPLS()
