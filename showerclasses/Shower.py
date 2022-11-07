from dataclasses import dataclass
from Material import Material
import numpy as np

@dataclass
class Shower:
"""Shower Object
Contains several methods for the showering and a shower state object
shower_state = [(E,Pos,particle type)]

"""
    surface : Material
    initial_e : float
    shower_state = np.array([(initial_e,0.0,11)])
    
    def size(self):
        """Return the number of particles currently in the shower
        """
        return len(shower_state)

    def clear_parent(self,int: indx):
        """Clear parent particle from shower
        """
        pass

    def propagate(self):
        """Propoagate shower
        """
        pass

    def clear_part(self,indx):
        """Clear particle from the shower (because it has left the material)
        """
        pass


    def lepton_num(self):
        """Return lepton number from shower
        """
        return None
