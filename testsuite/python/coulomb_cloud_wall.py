
#
# Copyright (C) 2013,2014,2015,2016 The ESPResSo project
#
# This file is part of ESPResSo.
#
# ESPResSo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ESPResSo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Tests particle property setters/getters
from __future__ import print_function
import unittest as ut
import espressomd
import numpy as np
from espressomd.electrostatics import *
from espressomd import scafacos


class CoulombCloudWall(ut.TestCase):
    if "ELECTROSTATICS" in espressomd.features():
        """This compares p3m, p3m_gpu, scafacos_p3m and scafacos_p2nfft 
           electrostatic forces and energy against stored data."""
        S = espressomd.System()
        forces = {}
        tolerance = 1E-3

        # Reference energy from p3m in the tcl test case
        reference_energy = 148.94229549

        def setUp(self):
            self.S.box_l = (10, 10, 10)
            self.S.time_step = 0.01
            self.S.cell_system.skin = 0.4

            #  Clear actors that might be left from prev tests
            if len(self.S.actors):
                del self.S.actors[0]
            self.S.part.clear()
            data = np.genfromtxt("data/coulomb_cloud_wall_system.data")

            # Add particles to system and store reference forces in hash
            # Input format: id pos q f
            for particle in data:
                id = particle[0]
                pos = particle[1:4]
                q = particle[4]
                f = particle[5:]
                self.S.part.add(id=int(id), pos=pos, q=q)
                self.forces[id] = f

        def compare(self, method_name, energy=True):
            # Compare forces and energy now in the system to stored ones

            # Force
            force_abs_diff = 0.
            for p in self.S.part:
                force_abs_diff += abs(np.sqrt(sum((p.f - self.forces[p.id])**2)))
            force_abs_diff /= len(self.S.part)

            print(method_name, "force difference", force_abs_diff)

            # Energy
            if energy:
                energy_abs_diff = abs(self.S.analysis.energy(
                    self.S)["total"] - self.reference_energy)
                print(method_name, "energy difference", energy_abs_diff)
                self.assertTrue(energy_abs_diff <= self.tolerance, "Absolte energy difference " +
                                str(energy_abs_diff) + " too large for " + method_name)
            self.assertTrue(force_abs_diff <= self.tolerance, "Asbolute force difference " +
                            str(force_abs_diff) + " too large for method " + method_name)

        # Tests for individual methods

        if "P3M" in espressomd.features():
            def test_p3m(self):
                self.S.actors.add(P3M(bjerrum_length=1, r_cut=1.001, accuracy = 1e-3,
                                      mesh=64, cao=7, alpha=2.70746, tune=False))
                self.S.integrator.run(0)
                self.compare("p3m", energy=True)

        if "ELECTROSTATICS" in espressomd.features() and "CUDA" in espressomd.features():
            def test_p3m_gpu(self):
                self.S.actors.add(P3M_GPU(bjerrum_length=1, r_cut=1.001, accuracy = 1e-3,
                                          mesh=64, cao=7, alpha=2.70746, tune=False))
                self.S.integrator.run(0)
                self.compare("p3m_gpu", energy=False)

        if "SCAFACOS" in espressomd.features():
            if "p3m" in scafacos.available_methods():
                def test_scafacos_p3m(self):
                    self.S.actors.add(Scafacos(bjerrum_length=1, method_name="p3m", method_params={
                                      "p3m_r_cut": 1.001, "p3m_grid": 64, "p3m_cao": 7, "p3m_alpha": 2.70746}))
                    self.S.integrator.run(0)
                    self.compare("scafacos_p3m", energy=True)

            if "p2nfft" in scafacos.available_methods():
                def test_scafacos_p2nfft(self):
                    self.S.actors.add(Scafacos(bjerrum_length=1, method_name="p2nfft", method_params={
                                      "p2nfft_r_cut": 1.001, "tolerance_field": 1E-4}))
                    self.S.integrator.run(0)
                    self.compare("scafacos_p2nfft", energy=True)

        def test_zz_deactivation(self):
            # Is the energy 0, if no methods active
            self.assertTrue(self.S.analysis.energy(self.S)["total"] == 0.0)


if __name__ == "__main__":
    ut.main()
