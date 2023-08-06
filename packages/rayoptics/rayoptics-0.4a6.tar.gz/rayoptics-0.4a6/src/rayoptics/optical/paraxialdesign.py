#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Michael J. Hayford
""" First order paraxial design space

.. Created on Sat Mar 31 21:14:42 2018

.. codeauthor: Michael J. Hayford
"""

from collections import namedtuple


from rayoptics.optical.model_constants import ht, slp, aoi
from rayoptics.optical.model_constants import pwr, tau, indx, rmd
from rayoptics.optical.model_constants import Intfc, Gap, Indx
from rayoptics.optical.elements import insert_ifc_gp_ele
from rayoptics.optical.surface import InteractionMode as imode

ParaxData = namedtuple('ParaxData', ['ht', 'slp', 'aoi'])
""" paraxial ray data at an interface

    Attributes:
        ht: height at interface
        slp: n*slope
        aoi: n*angle of incidence
"""

ParaxSys = namedtuple('ParaxSys', ['pwr', 'tau', 'indx', 'rmd'])
""" paraxial lens data at an interface

    Attributes:
        pwr: power
        tau: reduced distance, t/n
        indx: refractive index (n)
        rmd: refract mode
"""


class ParaxialModel():
    def __init__(self, opt_model):
        self.opt_model = opt_model
        self.seq_model = opt_model.seq_model
        self.sys = None
        self.ax = []
        self.pr = []
        self.opt_inv = 1.0

    def __json_encode__(self):
        attrs = dict(vars(self))
        del attrs['opt_model']
        del attrs['seq_model']
        del attrs['parax_data']
        return attrs

    def sync_to_restore(self, opt_model):
        self.opt_model = opt_model

    def update_model(self):
        self.parax_data = self.opt_model.optical_spec.parax_data
        self.build_lens()

    def build_lens(self):
        self.sys = self.seq_model_to_paraxial_lens()
        sys = self.sys
        ax_ray, pr_ray, fod = self.parax_data
        self.opt_inv = fod.opt_inv

        self.ax = []
        self.pr = []
        for i in range(0, len(sys)):
            n = sys[i][indx]
            self.ax.append([ax_ray[i][ht], n*ax_ray[i][slp], n*ax_ray[i][aoi]])
            self.pr.append([pr_ray[i][ht], n*pr_ray[i][slp], n*pr_ray[i][aoi]])

    def add_node(self, surf, new_vertex, type_sel, factory):
        """ Add a node in the paraxial data structures and the sequential model """
        ns = self.seq_model.get_num_surfaces()
        if surf >= ns - 1:
            surf = ns - 2
        n = self.sys[surf][indx]
        new_surf = surf + 1
        self.sys.insert(new_surf, [0.0, 0.0, n, ''])

        ax_node = [0.0, 0.0, 0.0]
        ax_node[type_sel] = new_vertex[1]
        self.ax.insert(new_surf, ax_node)

        pr_node = [0.0, 0.0, 0.0]
        pr_node[type_sel] = new_vertex[0]
        self.pr.insert(new_surf, pr_node)

        seq, ele = factory()
        insert_ifc_gp_ele(self.opt_model, seq, ele, idx=surf)

        self.sys[new_surf][rmd] = seq[0][0].interact_mode
        if seq[0][0].interact_mode == imode.Reflect:
            self.sys[new_surf][indx] = -self.sys[new_surf][indx]

    def delete_node(self, surf):
        """ delete the node at position surf """
        del self.sys[surf]
        del self.ax[surf]
        del self.pr[surf]

    def apply_ht_dgm_data(self, surf, new_vertex=None):
        """ This routine calculates all data dependent on the input
            height coordinates (y,ybar) at surface surf.
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr
        opt_inv = self.opt_inv

        if new_vertex is not None:
            pr_ray[surf][ht] = new_vertex[0]
            ax_ray[surf][ht] = new_vertex[1]

        nsm1 = len(sys) - 1
        if surf == 0:
            surf += 1

        p = surf - 1
        c = surf

        sys[p][tau] = ((ax_ray[p][ht]*pr_ray[c][ht] -
                        ax_ray[c][ht]*pr_ray[p][ht]) / opt_inv)
        ax_ray[p][slp] = (ax_ray[c][ht] - ax_ray[p][ht])/sys[p][tau]
        pr_ray[p][slp] = (pr_ray[c][ht] - pr_ray[p][ht])/sys[p][tau]

        if (surf > 1):
            p2 = surf - 2
            sys[p][pwr] = ((ax_ray[p2][slp]*pr_ray[p][slp] -
                            ax_ray[p][slp]*pr_ray[p2][slp])
                           / opt_inv)

        if (surf < nsm1):
            s = surf + 1

            sys[c][tau] = (ax_ray[c][ht]*pr_ray[s][ht] -
                           ax_ray[s][ht]*pr_ray[c][ht])/opt_inv
            ax_ray[c][slp] = (ax_ray[s][ht] - ax_ray[c][ht])/sys[c][tau]
            pr_ray[c][slp] = (pr_ray[s][ht] - pr_ray[c][ht])/sys[c][tau]
            sys[c][pwr] = (ax_ray[p][slp]*pr_ray[c][slp] -
                           ax_ray[c][slp]*pr_ray[p][slp])/opt_inv

            sys[s][pwr] = (ax_ray[c][slp]*pr_ray[s][slp] -
                           ax_ray[s][slp]*pr_ray[c][slp])/opt_inv

        else:
            ax_ray[c][slp] = ax_ray[p][slp]
            pr_ray[c][slp] = pr_ray[p][slp]
            sys[c][pwr] = 0
            sys[c][tau] = 0

    def apply_slope_dgm_data(self, surf, new_vertex=None):
        """ This routine calculates all data dependent on the input
            slope coordinates (nu,nubar) at surface surf.
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr
        opt_inv = self.opt_inv

        if new_vertex is not None:
            pr_ray[surf][slp] = new_vertex[0]
            ax_ray[surf][slp] = new_vertex[1]

        nsm1 = len(sys) - 1
        if nsm1 == 0:
            p = 0
            c = 1
            ax_ray[c][ht] = ax_ray[p][slp]*sys[p][tau] + ax_ray[p][ht]
            pr_ray[c][ht] = pr_ray[p][slp]*sys[p][tau] + pr_ray[p][ht]

        else:
            if (surf == 0):
                surf += 1

            p = surf - 1
            c = surf

            sys[c][pwr] = (ax_ray[p][slp]*pr_ray[c][slp] -
                           ax_ray[c][slp]*pr_ray[p][slp])/opt_inv
            ax_ray[c][ht] = (ax_ray[p][slp] - ax_ray[c][slp])/sys[c][pwr]
            pr_ray[c][ht] = (pr_ray[p][slp] - pr_ray[c][slp])/sys[c][pwr]
            sys[p][tau] = (ax_ray[p][ht]*pr_ray[c][ht] -
                           ax_ray[c][ht]*pr_ray[p][ht])/opt_inv

            if (surf < nsm1):
                s = surf + 1
                ax_ray[s][ht] = ax_ray[c][slp]*sys[c][tau] + ax_ray[c][ht]
                pr_ray[s][ht] = pr_ray[c][slp]*sys[c][tau] + pr_ray[c][ht]

    # ParaxTrace() - This routine performs a paraxial raytrace from object
    #                (surface 0) to image.  The last operation is a
    #                transfer to the image surface.
    def paraxial_trace(self):
        """ regenerate paraxial axial and chief rays from power and reduced
            distance
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr

        nsm1 = len(sys) - 1

        # Transfer from object
        c = 0
        s = 1
        ax_ray[s][ht] = ax_ray[c][ht] + sys[c][tau]*ax_ray[c][slp]
        pr_ray[s][ht] = pr_ray[c][ht] + sys[c][tau]*pr_ray[c][slp]

        for i in range(1, len(sys)):

            p = c
            c = s

            # Refraction
            ax_ray[c][slp] = ax_ray[p][slp] - ax_ray[c][ht]*sys[c][pwr]
            pr_ray[c][slp] = pr_ray[p][slp] - pr_ray[c][ht]*sys[c][pwr]

            # Transfer
            if (i < nsm1):
                s += 1
                ax_ray[s][ht] = ax_ray[c][ht] + sys[c][tau]*ax_ray[c][slp]
                pr_ray[s][ht] = pr_ray[c][ht] + sys[c][tau]*pr_ray[c][slp]

    def list_lens(self):
        """ list the paraxial axial and chief rays, and power, reduced distance
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr

        print("      ax_ray_ht    ax_ray_slp")
        for i in range(0, len(ax_ray)):
            print("{}: {:12.5g}  {:12.6g}".format(i, ax_ray[i][ht],
                  ax_ray[i][slp]))

        print("\n      pr_ray_ht    pr_ray_slp")
        for i in range(0, len(pr_ray)):
            print("{}: {:12.5g}  {:12.6g}".format(i, pr_ray[i][ht],
                  pr_ray[i][slp]))

        print("\n           power           tau        index    type")
        for i in range(0, len(sys)):
            print("{}: {:13.7g}  {:12.5g} {:12.5f}    {}".format(i,
                  sys[i][pwr], sys[i][tau], sys[i][indx], sys[i][rmd].name))

    def seq_model_to_paraxial_lens(self):
        """ returns lists of power, reduced thickness, signed index and refract
            mode
        """
        sys = []
        for i, sg in enumerate(self.seq_model.path()):
            if sg[Gap]:
                n_after = sg[Indx]
                tau = sg[Gap].thi/n_after
                rmode = sg[Intfc].interact_mode
                power = sg[Intfc].optical_power
                sys.append([power, tau, n_after, rmode])
            else:
                sys.append([0.0, 0.0, n_after, sg[Intfc].interact_mode])
        return sys

    def paraxial_lens_to_seq_model(self):
        """ Applies a paraxial lens spec (power, reduced distance) to the model
        """
        sys = self.sys
        ax_ray = self.ax
        n_before = sys[0][indx]
        slp_before = self.ax[0][slp]
        for i, sg in enumerate(self.seq_model.path()):
            if sg[Gap]:
                n_after = sys[i][indx]
                slp_after = ax_ray[i][slp]
                sg[Gap].thi = n_after*sys[i][tau]

                sg[Intfc].set_optical_power(sys[i][pwr], n_before, n_after)
                sg[Intfc].from_first_order(slp_before, slp_after,
                                           ax_ray[i][ht])

                n_before = n_after
                slp_before = slp_after

    def pwr_slope_solve(self, ray, surf, slp_new):
        p = ray[surf-1]
        c = ray[surf]
        pwr = (p[slp] - slp_new)/c[ht]
        return pwr

    def pwr_ht_solve(self, ray, surf, ht_new):
        sys = self.sys
        p = ray[surf-1]
        c = ray[surf]
        slp_new = (ht_new - c[ht])/sys[surf][tau]
        pwr = (p[slp] - slp_new)/ht_new
        return pwr

    def thi_ht_solve(self, ray, surf, ht_new):
        c = ray[surf]
        thi = (ht_new - c[ht])/c[slp]
        return thi

    def apply_data(self, vertex, lcl_pt):
        ray = self.ray
        p = ray[vertex-1]
        c = ray[vertex]
        c_slp_new = (lcl_pt[1] - c[ht])/lcl_pt[0]
        pwr = (p[slp] - c_slp_new)/c[ht]
        self.opt_model.seq_model.ifcs[vertex].optical_power = pwr
