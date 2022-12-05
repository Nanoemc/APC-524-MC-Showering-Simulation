from dataclasses import dataclass
from Material import Material
import numpy as np


@dataclass
class Shower:
    """Shower Object
    shower_state = [(E,Pos,particle type/id)]
    """

    surface: Material
    initial_e: float  # (in MeV)

    def __post_init__(self):
        self.shower_state = [(self.initial_e, 0.0, 11)]
        self.e_disp = 0

    def size(self):
        """Return the number of particles currently in the shower"""
        return len(self.shower_state)

    def shower_surface(self):
        """Return the surface object associated with the shower"""
        return self.surface

    def crnt_shower(self):
        """Return current shower state"""
        return self.shower_state

    def beta(self, E: float, mass=0.511):
        """Obtain the propagation speed of an electron/positron"""
        return np.sqrt(1 - mass**2 / E**2)

    def ionization_loss(self, delta_x: float, beta: float):
        """Determine energy loss of an electron/positron due to ionization
        Here delta_x is taken to be in cm and dE/dx is assumed to be constant for showering leptons
        """
        return self.surface.dens() * 2 * delta_x * 1 / beta**2

    def propagate(self):
        """Propagate shower
        Method will modify the shower object by propagating each of the constituent particles of the shower
        """
        part_indx = 0
        parent_size = self.size()
        # for part in self.shower_state:
        for i in range(parent_size):
            part = self.shower_state[0]
            if abs(part[2]) == 11:
                prop_len = self.surface.radlen()
                if abs(part[0] > self.surface.e_crit()):
                    # print("Bremsstrahlung")
                    self.shower_state.append((part[0] / 2, part[1] + prop_len, part[2]))
                    self.shower_state.append((part[0] / 2, part[1] + prop_len, 22))

                    # Shower Leakage
                    if part[1] + prop_len > self.surface.len():
                        print("Shower Leakage")
                        del self.shower_state[self.shower_state.size() - 1]
                        del self.shower_state[self.shower_state.size() - 1]

                    # Ionization loss should be calculated here so that shower leakage can be accounted for (if needed)

                    # Remove parent particle
                    del self.shower_state[0]
                    part_indx += 1

                elif part[0] < self.surface.e_crit():
                    # print("electron/positron is no longer showering")
                    del self.shower_state[0]

                continue

            if part[2] == 22:
                prop_len = self.surface.radlen()
                if part[0] > 2 * 0.511:
                    self.shower_state.append((part[0] / 2, part[1] + prop_len, 11))
                    self.shower_state.append((part[0] / 2, part[1] + prop_len, -11))

                    # Shower Leakage
                    if part[1] + prop_len > self.surface.len():
                        print("Shower Leakage")
                        del self.shower_state[self.shower_state.size() - 1]
                        del self.shower_state[self.shower_state.size() - 1]

                    # Remove parent particle
                    del self.shower_state[0]
                    part_indx += 1

                elif part[0] <= 2 * 0.511:
                    # print("Photon is no longer showering")
                    del self.shower_state[0]

                continue

    def lepton_num(self):
        """Return lepton number from shower"""
        lepnum = 0
        for part in self.shower_state:
            if abs(part[2]) == 11:
                lepnum += part[2] / 11
        return int(lepnum)

    def lepton_count(self):
        """Return the total number of electrons and positrons in the shower"""
        lepcount = 0
        for part in self.shower_state:
            if abs(part[2]) == 11:
                lepcount += 1
        return lepcount

    def photon_count(self):
        """Return the total number of electrons and positrons in the shower"""
        photo_count = 0
        for part in self.shower_state:
            if part[2] == 22:
                photo_count += 1
        return photo_count
