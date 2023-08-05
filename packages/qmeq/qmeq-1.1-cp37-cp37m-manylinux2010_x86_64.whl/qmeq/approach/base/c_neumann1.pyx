# cython: boundscheck=False
# cython: cdivision=True
# cython: infertypes=False
# cython: initializedcheck=False
# cython: nonecheck=False
# cython: profile=False
# cython: wraparound=False

"""Module containing cython functions, which generate first order 1vN kernel.
   For docstrings see documentation of module neumann1."""

# Python imports

import numpy as np
import itertools

from ...wrappers.mytypes import doublenp
from ...wrappers.mytypes import complexnp

# Cython imports

cimport numpy as np
cimport cython

from ...specfunc.c_specfunc cimport func_1vN

from ..c_aprclass cimport Approach
from ..c_kernel_handler cimport KernelHandler

# ---------------------------------------------------------------------------------------------------
# 1 von Neumann approach
# ---------------------------------------------------------------------------------------------------
cdef class Approach1vN(Approach):

    kerntype = '1vN'

    cdef void prepare_arrays(self):
        Approach.prepare_arrays(self)
        nleads, ndm1 = self.si.nleads, self.si.ndm1
        self.phi1fct = np.zeros((nleads, ndm1, 2), dtype=complexnp)
        self.phi1fct_energy = np.zeros((nleads, ndm1, 2), dtype=complexnp)
        self.phi1 = np.zeros((nleads, ndm1), dtype=complexnp)

        self._phi1fct = self.phi1fct
        self._phi1fct_energy = self.phi1fct_energy
        self._phi1 = self.phi1
        self._rez_complex = np.zeros(4, dtype=complexnp)

    cdef void clean_arrays(self):
        Approach.clean_arrays(self)
        self._phi1fct[::1] = 0.0
        self._phi1fct_energy[::1] = 0.0
        self._phi1[::1] = 0.0

    cpdef void generate_fct(self):
        cdef double_t [:] E = self._Ea
        cdef double_t [:] mulst = self._mulst
        cdef double_t [:] tlst = self._tlst
        cdef double_t [:, :] dlst = self._dlst

        cdef KernelHandler kh = self._kernel_handler
        cdef long_t nleads = kh.nleads

        cdef long_t itype = self.funcp.itype
        cdef int_t limit = self.funcp.dqawc_limit

        cdef long_t c, b, bcharge, cb, l
        cdef double_t Ecb

        cdef complex_t [:, :, :] phi1fct = self._phi1fct
        cdef complex_t [:, :, :] phi1fct_energy = self._phi1fct_energy
        cdef complex_t [:] rez = self._rez_complex

        for i in range(kh.ndm1):
            c = kh.all_ba[i, 0]
            b = kh.all_ba[i, 1]
            bcharge = kh.all_ba[i, 2]
            cb = kh.get_ind_dm1(c, b, bcharge)
            Ecb = E[c]-E[b]
            for l in range(nleads):
                func_1vN(Ecb, mulst[l], tlst[l], dlst[l, 0], dlst[l, 1], itype, limit, rez)
                phi1fct[l, cb, 0] = rez[0]
                phi1fct[l, cb, 1] = rez[1]
                phi1fct_energy[l, cb, 0] = rez[2]
                phi1fct_energy[l, cb, 1] = rez[3]

    cdef void generate_coupling_terms(self,
                long_t b, long_t bp, long_t bcharge,
                KernelHandler kh) nogil:

        cdef long_t a, ap, bpp, c, cp, \
                    ba, bap, bpa, cb, cbp, cpb
        cdef complex_t fct_aap, fct_bppbp, fct_bbpp, fct_ccp

        cdef long_t i, j, l
        cdef long_t nleads = kh.nleads
        cdef long_t [:, :] statesdm = kh.statesdm

        cdef complex_t [:, :, :] phi1fct = self._phi1fct
        cdef complex_t [:, :, :] Tba = self._Tba

        cdef long_t acharge = bcharge-1
        cdef long_t ccharge = bcharge+1

        cdef long_t acount = kh.statesdm_count[acharge] if acharge >= 0 else 0
        cdef long_t bcount = kh.statesdm_count[bcharge]
        cdef long_t ccount = kh.statesdm_count[ccharge] if ccharge <= kh.ncharge else 0

        # --------------------------------------------------
        for i in range(acount):
            for j in range(acount):
                a = statesdm[acharge, i]
                ap = statesdm[acharge, j]
                if not kh.is_included(a, ap, acharge):
                    continue
                bpa = kh.get_ind_dm1(bp, a, acharge)
                bap = kh.get_ind_dm1(b, ap, acharge)
                fct_aap = 0
                for l in range(nleads):
                    fct_aap += (+ Tba[l, b, a]*Tba[l, ap, bp]*phi1fct[l, bpa, 0].conjugate()
                                - Tba[l, b, a]*Tba[l, ap, bp]*phi1fct[l, bap, 0])
                kh.set_matrix_element(fct_aap, b, bp, bcharge, a, ap, acharge)
        # --------------------------------------------------
        for i in range(bcount):
            bpp = statesdm[bcharge, i]
            if kh.is_included(bpp, bp, bcharge):
                fct_bppbp = 0
                for j in range(acount):
                    a = statesdm[acharge, j]
                    bpa = kh.get_ind_dm1(bp, a, acharge)
                    for l in range(nleads):
                        fct_bppbp += +Tba[l, b, a]*Tba[l, a, bpp]*phi1fct[l, bpa, 1].conjugate()
                for j in range(ccount):
                    c = statesdm[ccharge, j]
                    cbp = kh.get_ind_dm1(c, bp, bcharge)
                    for l in range(nleads):
                        fct_bppbp += +Tba[l, b, c]*Tba[l, c, bpp]*phi1fct[l, cbp, 0]
                kh.set_matrix_element(fct_bppbp, b, bp, bcharge, bpp, bp, bcharge)
            # --------------------------------------------------
            if kh.is_included(b, bpp, bcharge):
                fct_bbpp = 0
                for j in range(acount):
                    a = statesdm[acharge, j]
                    ba = kh.get_ind_dm1(b, a, acharge)
                    for l in range(nleads):
                        fct_bbpp += -Tba[l, bpp, a]*Tba[l, a, bp]*phi1fct[l, ba, 1]
                for j in range(ccount):
                    c = statesdm[ccharge, j]
                    cb = kh.get_ind_dm1(c, b, bcharge)
                    for l in range(nleads):
                        fct_bbpp += -Tba[l, bpp, c]*Tba[l, c, bp]*phi1fct[l, cb, 0].conjugate()
                kh.set_matrix_element(fct_bbpp, b, bp, bcharge, b, bpp, bcharge)
        # --------------------------------------------------
        for i in range(ccount):
            for j in range(ccount):
                c = statesdm[ccharge, i]
                cp = statesdm[ccharge, j]
                if not kh.is_included(c, cp, ccharge):
                    continue
                cbp = kh.get_ind_dm1(c, bp, bcharge)
                cpb = kh.get_ind_dm1(cp, b, bcharge)
                fct_ccp = 0
                for l in range(nleads):
                    fct_ccp += (+ Tba[l, b, c]*Tba[l, cp, bp]*phi1fct[l, cbp, 1]
                                - Tba[l, b, c]*Tba[l, cp, bp]*phi1fct[l, cpb, 1].conjugate())
                kh.set_matrix_element(fct_ccp, b, bp, bcharge, c, cp, ccharge)
        # --------------------------------------------------

    cpdef void generate_current(self):
        cdef double_t [:] E = self._Ea
        cdef complex_t [:, :, :] Tba = self._Tba

        cdef complex_t [:, :, :] phi1fct = self._phi1fct
        cdef complex_t [:, :, :] phi1fct_energy = self._phi1fct_energy

        cdef long_t i, j, l
        cdef long_t bcharge, ccharge, bcount, ccount
        cdef long_t b, bp, c, cp, cb
        cdef complex_t fct1, fct2, fct1h, fct2h, phi0bpb, phi0ccp

        cdef KernelHandler kh = self._kernel_handler
        cdef long_t [:, :] statesdm = kh.statesdm
        cdef long_t nleads = kh.nleads

        cdef complex_t [:, :] phi1 = self._phi1
        cdef double_t [:] current = self._current
        cdef double_t [:] energy_current = self._energy_current
        cdef double_t [:] heat_current = self._heat_current

        cdef complex_t current_l, energy_current_l, phi1_l

        for i in range(kh.ndm1):
            c = kh.all_ba[i, 0]
            b = kh.all_ba[i, 1]

            bcharge = kh.all_ba[i, 2]
            ccharge = bcharge+1

            bcount = kh.statesdm_count[bcharge]
            ccount = kh.statesdm_count[ccharge] if ccharge <= kh.ncharge else 0

            cb = kh.get_ind_dm1(c, b, bcharge)

            for l in range(nleads):
                current_l, energy_current_l, phi1_l = 0, 0, 0

                fct1 = phi1fct[l, cb, 0]
                fct2 = phi1fct[l, cb, 1]
                fct1h = phi1fct_energy[l, cb, 0]
                fct2h = phi1fct_energy[l, cb, 1]

                for j in range(bcount):
                    bp = statesdm[bcharge, j]
                    if not kh.is_included(bp, b, bcharge):
                        continue
                    phi0bpb = kh.get_phi0_element(bp, b, bcharge)

                    phi1_l += Tba[l, c, bp]*phi0bpb*fct1
                    current_l += Tba[l, b, c]*Tba[l, c, bp]*phi0bpb*fct1
                    energy_current_l += Tba[l, b, c]*Tba[l, c, bp]*phi0bpb*fct1h

                for j in range(ccount):
                    cp = statesdm[ccharge, j]
                    if not kh.is_included(c, cp, ccharge):
                        continue
                    phi0ccp = kh.get_phi0_element(c, cp, ccharge)

                    phi1_l += Tba[l, cp, b]*phi0ccp*fct2
                    current_l += Tba[l, b, c]*phi0ccp*Tba[l, cp, b]*fct2
                    energy_current_l += Tba[l, b, c]*phi0ccp*Tba[l, cp, b]*fct2h

                phi1[l, cb] = phi1[l, cb] + phi1_l
                current[l] += -2*current_l.imag
                energy_current[l] += -2*energy_current_l.imag

        for l in range(nleads):
            heat_current[l] = energy_current[l] - current[l]*self._mulst[l]
# ---------------------------------------------------------------------------------------------------
