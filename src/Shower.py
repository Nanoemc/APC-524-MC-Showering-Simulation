from dataclasses import dataclass
from Material_Prop import Material
import numpy as np
from datetime import datetime


@dataclass
class Shower:
    """Shower Object
    This object represents the state of an electromagnetic shower. The object itself is an array of tuples
    where the tuple contains the energy of the particle, its position, and the particle type.
    shower_state = [(E,Pos,particle type/id)]

    Parameters
    ----------
    surface: Material
    initial_e: float
    verbose: bool
    write_to_file: bool
    file_name: str


    """

    surface: Material
    initial_e: float  # (in MeV)
    verbose: bool = False
    write_to_file: bool = False
    file_name: str = "em_shower_" + str(datetime.today()) + ".csv"

    def __post_init__(self):
        self.shower_state = [(self.initial_e, 0.0, 11)]
        self.e_disp = 0
        if self.verbose and self.initial_e < self.surface.e_crit():
            print(
                "!!Initial electron energy less than the critical energy of the material!!"
            )
            print("!!No shower development will occur in this system!!")

    def size(self):
        """Return the number of particles currently in the shower"""
        return len(self.shower_state)

    def shower_surface(self):
        """Return the surface object associated with the shower"""
        return self.surface

    def crnt_shower(self):
        """Return current shower state array"""
        return self.shower_state

    def beta(self, energy: float, mass: float = 0.511):
        """Obtain the propagation speed of an electron/positron

        Parameters
        ----------
        energy : float
        mass: float

        Returns
        -------
        float
        Returns the velocity of the particle as a multiple of the speed of light
        """
        return np.sqrt(1 - mass**2 / energy**2)

    def ionization_loss(self, delta_x: float, beta: float):
        """Determine energy loss of an electron/positron due to ionization
        Here delta_x is taken to be in cm and dE/dx is assumed to be constant for showering leptons

        Parameters
        ----------
        delta_x: float
        beta: float

        Returns
        -------
        float
        Returns the energy loss due to ionization of a charged lepton


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

            if abs(part[2]) == 11:  # electron/positron
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

                    self.e_disp += self.ionization_loss(
                        prop_dist_x0, self.beta(part[0])
                    )  # Ionization loss

                    # Remove parent particle
                    del self.shower_state[0]
                    part_indx += 1

                elif part[0] < self.surface.e_crit():
                    if self.verbose:
                        print("electron/positron is no longer showering")
                    del self.shower_state[0]

                continue

            if part[2] == 22:  # Photon
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
