from dataclasses import dataclass


@dataclass
class Material:
    """Material Object"""

    length: float
    material: str

    def len(self):
        """Return length of the material in cm"""
        return self.length

    def dens(self):
        """Return density of the material in g/cm^3"""
        return 1

    def len_x0(self):
        """Return length of material in units of radiation lengths"""
        return self.length / self.radlen_cm()  # Length in units of radiation length

    def dist_to_x0(self, x: float):
        """Return a distance in radiation lengths"""
        return x / self.radlen_cm()

    def radlen_cm(self):
        """Return radiaiton length of material in cm"""
        return 41.31  # Radiation Length in cm (polystyrene)

    def radlen(self):
        """Return radiaiton length of material in g cm^-2"""
        return 43.79  # g cm^-2

    def e_crit(self):
        """Return Critical Energy in MeV"""
        return 93.11  # MeV (polystyrene)
