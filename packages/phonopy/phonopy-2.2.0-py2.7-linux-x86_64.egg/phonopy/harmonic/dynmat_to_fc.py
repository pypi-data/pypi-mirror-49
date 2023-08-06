# Copyright (C) 2014 Atsushi Togo
# All rights reserved.
#
# This file is part of phonopy.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from phonopy.structure.atoms import PhonopyAtoms
from phonopy.structure.cells import get_supercell
from phonopy.harmonic.force_constants import distribute_force_constants
from phonopy.structure.cells import SNF3x3


def get_commensurate_points(supercell_matrix):  # wrt primitive cell
    """Commensurate q-points are returned.

    Parameters
    ----------
    supercell_matrix : array_like
        Supercell matrix with respect to primitive cell basis vectors.
        shape=(3, 3)
        dtype=intc

    """

    smat = np.array(supercell_matrix, dtype=int)
    rec_primitive = PhonopyAtoms(numbers=[1],
                                 scaled_positions=[[0, 0, 0]],
                                 cell=np.diag([1, 1, 1]),
                                 pbc=True)
    rec_supercell = get_supercell(rec_primitive, smat.T)
    q_pos = rec_supercell.get_scaled_positions()
    return np.array(np.where(q_pos > 1 - 1e-15, q_pos - 1, q_pos),
                    dtype='double', order='C')


def get_commensurate_points_in_integers(supercell_matrix):
    """Commensurate q-points in integer representation are returned.

    A set of integer representation of lattice points is transformed to
    the equivalent set of lattice points in fractional coordinates with
    respect to supercell basis vectors by
        integer_lattice_points / det(supercell_matrix)

    Parameters
    ----------
    supercell_matrix : array_like
        Supercell matrix with respect to primitive cell basis vectors.
        shape=(3, 3)
        dtype=intc

    Returns
    -------
    lattice_points : ndarray
        Integer representation of lattice points in supercell.
        shape=(N, 3)

    """
    smat = np.array(supercell_matrix, dtype=int)
    snf = SNF3x3(smat.T)
    snf.run()
    D = snf.A.diagonal()
    b, c, a = np.meshgrid(range(D[1]), range(D[2]), range(D[0]))
    lattice_points = np.dot(np.c_[a.ravel() * D[1] * D[2],
                                  b.ravel() * D[0] * D[2],
                                  c.ravel() * D[0] * D[1]], snf.Q.T)
    lattice_points = np.array(lattice_points % np.prod(D),
                              dtype='intc', order='C')
    return lattice_points


class DynmatToForceConstants(object):
    def __init__(self,
                 primitive,
                 supercell,
                 frequencies=None,
                 eigenvectors=None,
                 is_full_fc=True,
                 symprec=1e-5):
        self._primitive = primitive
        self._supercell = supercell
        supercell_matrix = np.linalg.inv(self._primitive.primitive_matrix)
        supercell_matrix = np.rint(supercell_matrix).astype('intc')
        self._commensurate_points = get_commensurate_points(supercell_matrix)
        (self._shortest_vectors,
         self._multiplicity) = primitive.get_smallest_vectors()
        self._dynmat = None
        n_s = self._supercell.get_number_of_atoms()
        n_p = self._primitive.get_number_of_atoms()
        if is_full_fc:
            fc_shape = (n_s, n_s, 3, 3)
        else:
            fc_shape = (n_p, n_s, 3, 3)
        self._fc = np.zeros(fc_shape, dtype='double', order='C')

        itemsize = self._fc.itemsize
        self._dtype_complex = ("c%d" % (itemsize * 2))

        if frequencies is not None and eigenvectors is not None:
            self.set_dynamical_matrices(frequencies, eigenvectors)

    def run(self):
        self._inverse_transformation()
        # Full fc
        # self._distribute_force_constants()

    def get_force_constants(self):
        return self._fc

    def get_commensurate_points(self):
        return self._commensurate_points

    def get_dynamical_matrices(self):
        return self._dynmat

    def set_dynamical_matrices(self,
                               frequencies_at_qpoints=None,
                               eigenvectors_at_qpoints=None,
                               dynmat=None):
        if dynmat is None:
            dm = []
            for frequencies, eigvecs in zip(frequencies_at_qpoints,
                                            eigenvectors_at_qpoints):
                eigvals = frequencies ** 2 * np.sign(frequencies)
                dm.append(
                    np.dot(np.dot(eigvecs, np.diag(eigvals)),
                           eigvecs.T.conj()))
        else:
            dm = dynmat

        self._dynmat = np.array(dm, dtype=self._dtype_complex, order='C')

    def _inverse_transformation(self):
        try:
            import phonopy._phonopy as phonoc
            self._c_inverse_transformation()
        except ImportError:
            self._py_inverse_transformation()

        if self._fc.shape[0] == self._fc.shape[1]:
            distribute_force_constants_by_translations(self._fc,
                                                       self._primitive,
                                                       self._supercell)

    def _c_inverse_transformation(self):
        import phonopy._phonopy as phonoc

        s2p = self._primitive.get_supercell_to_primitive_map()
        p2p = self._primitive.get_primitive_to_primitive_map()
        s2pp = np.array([p2p[i] for i in s2p], dtype='intc')

        if self._fc.shape[0] == self._fc.shape[1]:
            fc_index_map = self._primitive.get_primitive_to_supercell_map()
        else:
            fc_index_map = np.arange(self._fc.shape[0], dtype='intc')

        phonoc.transform_dynmat_to_fc(self._fc,
                                      self._dynmat.view(dtype='double'),
                                      self._commensurate_points,
                                      self._shortest_vectors,
                                      self._multiplicity,
                                      self._primitive.get_masses(),
                                      s2pp,
                                      fc_index_map)

    def _py_inverse_transformation(self):
        s2p = self._primitive.get_supercell_to_primitive_map()
        p2s = self._primitive.get_primitive_to_supercell_map()
        p2p = self._primitive.get_primitive_to_primitive_map()

        fc = self._fc
        m = self._primitive.get_masses()
        N = (self._supercell.get_number_of_atoms() /
             self._primitive.get_number_of_atoms())

        for p_i, s_i in enumerate(p2s):
            for s_j, p_j in enumerate([p2p[i] for i in s2p]):
                coef = np.sqrt(m[p_i] * m[p_j]) / N
                fc_elem = self._sum_q(p_i, s_j, p_j) * coef
                if fc.shape[0] == fc.shape[1]:
                    fc[s_i, s_j] = fc_elem
                else:
                    fc[p_i, s_j] = fc_elem

    def _sum_q(self, p_i, s_j, p_j):
        multi = self._multiplicity[s_j, p_i]
        pos = self._shortest_vectors[s_j, p_i, :multi]
        sum_q = np.zeros((3, 3), dtype=self._dtype_complex, order='C')
        phases = -2j * np.pi * np.dot(self._commensurate_points, pos.T)
        phase_factors = np.exp(phases).sum(axis=1) / multi
        for i, coef in enumerate(phase_factors):
            sum_q += self._dynmat[i,
                                  (p_i * 3):(p_i * 3 + 3),
                                  (p_j * 3):(p_j * 3 + 3)] * coef
        return sum_q.real


def distribute_force_constants_by_translations(fc, primitive, supercell):
    s2p = primitive.get_supercell_to_primitive_map()
    p2s = primitive.get_primitive_to_supercell_map()
    positions = supercell.get_scaled_positions()
    lattice = supercell.get_cell().T
    diff = positions - positions[p2s[0]]
    trans = np.array(diff[np.where(s2p == p2s[0])[0]],
                     dtype='double', order='C')
    rotations = np.array([np.eye(3, dtype='intc')] * len(trans),
                         dtype='intc', order='C')
    permutations = primitive.get_atomic_permutations()
    distribute_force_constants(fc,
                               p2s,
                               lattice,
                               rotations,
                               permutations)
