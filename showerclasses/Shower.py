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
    verbose: bool = False
    write_to_file: bool = False
    file_name: str = "test_shower.txt"

    def __post_init__(self):
        self.shower_state = [(self.initial_e, 0.0, 11)]
        self.e_disp = 0
        # if self.verbose == None:
        #     self.verbose = False
        # if self.write_to_file == None:
        #     self.write_to_file = False
        # if self.file_name == None and self.write_to_file == True:
        #     file_name = "test_shower.txt"

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
                prop_dist = self.surface.radlen()
                if abs(part[0] > self.surface.e_crit()):
                    if self.verbose:
                        print("Bremsstrahlung")
                    self.shower_state.append(
                        (part[0] / 2, part[1] + prop_dist, part[2])
                    )
                    self.shower_state.append((part[0] / 2, part[1] + prop_dist, 22))
                    prop_dist_x0 = self.surface.dist_to_x0(prop_dist)

                    # Shower Leakage
                    if part[1] + prop_dist > self.surface.len():
                        if self.verbose:
                            print("Shower Leakage")
                        prop_dist_x0 = self.surface.dist_to_x0(
                            part[1] + prop_dist - self.surface.len()
                        )
                        del self.shower_state[self.shower_state.size() - 1]
                        del self.shower_state[self.shower_state.size() - 1]

                    # Ionization loss should be calculated here so that shower leakage can be accounted for (if needed)
                    self.e_disp += ionization_loss(prop_dist_x0, self.beta(part[0]))

                    # Remove parent particle
                    del self.shower_state[0]
                    part_indx += 1

                elif part[0] < self.surface.e_crit():
                    if self.verbose:
                        print("electron/positron is no longer showering")
                    del self.shower_state[0]

                continue

            if part[2] == 22:
                prop_dist = self.surface.radlen()
                if part[0] > 2 * 0.511:
                    self.shower_state.append((part[0] / 2, part[1] + prop_dist, 11))
                    self.shower_state.append((part[0] / 2, part[1] + prop_dist, -11))

                    # Shower Leakage
                    if part[1] + prop_dist > self.surface.len():
                        if self.verbose:
                            print("Shower Leakage")
                        del self.shower_state[self.shower_state.size() - 1]
                        del self.shower_state[self.shower_state.size() - 1]

                    # Remove parent particle
                    del self.shower_state[0]
                    part_indx += 1

                elif part[0] <= 2 * 0.511:
                    if self.verbose:
                        print("Photon is no longer showering")
                    del self.shower_state[0]

                continue

        if self.write_to_file:
            if self.verbose:
                print("Writing shower to file")
            self.write_shower()

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
        """Return the total number of photons in the shower"""
        photo_count = 0
        for part in self.shower_state:
            if part[2] == 22:
                photo_count += 1
        return photo_count

    def write_shower(self):
        """Write current shower state to a file"""
        with open(self.file_name, "a") as f:
            for part in self.shower_state:
                print(str(part))
                f.write("%s," % str(part))
            f.write("\n")
