from dataclasses import dataclass

@dataclass
class Material:
"""Material Object 

"""
    length: float
    material: str

    def len_x0(self):
        """Return length of material in units of radiation lengths
        """
        return length/radlen_cm(self) #Length in units of radiation length

    def radlen_cm(self):
        """Return radiaiton length of material in cm
        """
        return 41.31 #Radiation Length in cm (polystyrene)
    
    def radlen(self):
        """Return radiaiton length of material in g cm^-2
        """
        return 43.79 #g cm^-2

    def e_crit(self):
        """Return Critical Energy in MeV
        """
        return 93.11 #MeV (polystyrene)


