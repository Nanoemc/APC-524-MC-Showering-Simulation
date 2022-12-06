import pytest
from math import log
import showerclass.Material
import showerclass.Shower


def lepton_num_test():
    block = Material(100 * 200, "")
    new_shower = Shower(surface=block, initial_e=50000)

    show_max = log2(50000 / new_shower.shower_surface.e_crit())
    gen = 0
    lepton_num = new_shower.lepton_num()

    while new_shower.size() != 0:
        new_shower.propagate()
        gen += 1

        if gen < shower_max:
            assert lepton_num == new_shower.lepton_num()


def particle_count_test():
    block = Material(100 * 200, "")
    new_shower = Shower(surface=block, initial_e=50000)

    while new_shower.size() != 0:
        new_shower.propagate()
        gen += 1
        assert new_shower.size() <= 2**gen


def energy_cons_test():
    return True
