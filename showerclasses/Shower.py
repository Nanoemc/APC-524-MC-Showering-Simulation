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

    def clear_parent(self,indx: int):
        """Clear parent particle from shower
        """
        pass

    def ionization_loss(self,delta_x):
        return None

    def propagate(self):
        """Propoagate shower
        Method will modify the shower class by propagating each of the contents of the shower
        """
        part_indx = 0
        for part in shower_state:
            prop_len = surface.radlen()
            if (abs(part[2]) == 11 && part[0] > surface.e_crit()):
                print("Bremsstrahlung")
                shower_state = np.append(shower_state,(part[0]/2, part[1] + prop_len),11)
                shower_state = np.append(shower_state,(part[0]/2, part[1] + prop_len),22)

                #Add check for shower leaks after each new particle is generated

                #Remove parent particle
                shower_state = np.delete(shower_state,0)
                part_indx += 1
            elif(abs(part[2]) == 11 && part[0] < surface.e_crit()):
                print("electron/positron is no longer showering")
                shower_state = np.delete(shower_state,0)

            if(part[2] == 22 && part[0] > 2*0.511):
                print("Pair Produce")
                shower_state = np.append(shower_state,(part[0]/2, part[1] + prop_len),11)
                shower_state = np.append(shower_state,(part[0]/2, part[1] + prop_len),-11)

                #Remove parent particle
                shower_state = np.delete(shower_state,0)
                part_indx += 1
            elif(part[2] == 22 && part[0] < 2*0.511):
                print("Photon is no longer showering")
                shower_state = np.delete(shower_state,0)


    def rem_part(self,indx: int):
        """Clear particle from the shower (because it has left the material)
        """
        shower_state = np.delete(shower_state,indx)


    def lepton_num(self):
        """Return lepton number from shower
        """
        lepnum = 0
        for part in shower_state:
            if abs(part[2] == 11):
                lepnum += part[2]

        return lepnum/11
