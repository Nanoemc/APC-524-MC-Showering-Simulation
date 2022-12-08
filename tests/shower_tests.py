import pytest
from math import log
import showerclass.Material
import showerclass.Shower


def lepton_num_cons_test():
    """Check lepton number is conserved while shower not attenuating"""
    block = Material(100 * 200, "")
    new_shower = Shower(surface=block, initial_e=50000)

    shower_max_depth = log2(50000 / new_shower.shower_surface.e_crit())
    shower_itr = 0
    lepton_num = new_shower.lepton_num()
    shower_size_list = [new_shower.size()]

    while new_shower.size() != 0:
        new_shower.propagate()
        shower_itr += 1
        shower_size_list.append(new_shower.size())

        if (
            shower_size_list[shower_itr] > shower_size_list[shower_itr - 1]
        ):  # Check while shower not attenuating
            assert lepton_num == new_shower.lepton_num()


def particle_count_test():
    """Check that the total number of particles never exceeds 2^N (limit from analytical model)"""
    block = Material(100 * 200, "")
    new_shower = Shower(surface=block, initial_e=50000)

    shower_itr = 0

    while new_shower.size() != 0:
        new_shower.propagate()
        shower_itr += 1
        assert new_shower.size() <= 2**shower_itr


def no_shower_test_energy():
    """Check an electron with less energy than the critical energy of a material does not shower"""
    block = Material(100 * 200, "")
    new_shower = Shower(surface=block, initial_e=5, verbose=True)
    shower_itr = 0

    while new_shower.size() != 0:
        new_shower.propagate()
        shower_itr += 1

    assert shower_itr == 1


def energy_cons_test():
    return True
