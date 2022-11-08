from dataclasses import dataclass
from Material import Material
import numpy as np

@dataclass
class Shower:
    """Shower Object
    Contains several methods for the showering and a shower state object
    shower_state = [(E,Pos,particle type/id)]
    """
    surface : Material
    initial_e : float


    def __post_init__(self):
        shower_state = np.array([(initial_e,0.0,11)])
        e_loss = 0
    
    def size(self):
        """Return the number of particles currently in the shower
        """
        return len(self.shower_state)


    def crnt_shower(self):
        """Return current shower state
        """
        return shower_state

    def beta(self,E : float,mass = 0.511):
        """Obtain the propagation speed of an electron/positron
        """
        return np.sqrt(1 - mass**2/E**2)

    def ionization_loss(self,delta_x : float, beta : float):
        """Determine energy loss of an electron/positron due to ionization
        Here delta_x is taken to be in cm and dE/dx is assumed to be constant for showering particles
        """
        return self.surface.dens()*2*delta_x*1/beta**2

    def propagate(self):
        """Propoagate shower
        Method will modify the shower class by propagating each of the contents of the shower
        """
        part_indx = 0
        for part in self.shower_state:
            if (part[2] == 11):
                prop_len = surface.radlen()
                if (abs(part[0] > surface.e_crit())):
                    print("Bremsstrahlung")
                    self.shower_state = np.append(self.shower_state,(part[0]/2, part[1] + prop_len),11)
                    self.shower_state = np.append(self.shower_state,(part[0]/2, part[1] + prop_len),22)

                    #Shower Leakage
                    if (prop_len > surface.len()):
                        print("Shower Leakage")
                        self.shower_state = np.delete(self.shower_state,self.size() - 1)
                        self.shower_state = np.delete(self.shower_state,self.size() - 1)

                    #Remove parent particle
                    self.shower_state = np.delete(self.shower_state,0)
                    part_indx += 1

                elif(part[0] < surface.e_crit()):
                    print("electron/positron is no longer showering")
                    self.shower_state = np.delete(self.shower_state,0)

            if (part[2] == 22):
                if(part[0] > 2*0.511):
                    print("Pair Produce")
                    self.shower_state = np.append(self.shower_state,(part[0]/2, part[1] + prop_len),11)
                    self.shower_state = np.append(self.shower_state,(part[0]/2, part[1] + prop_len),-11)

                    #Shower Leakage
                    if (prop_len > surface.len()):
                        print("Shower Leakage")
                        self.shower_state = np.delete(self.shower_state,self.size() - 1)
                        self.shower_state = np.delete(self.shower_state,self.size() - 1)

                    #Remove parent particle
                    self.shower_state = np.delete(self.shower_state,0)
                    part_indx += 1

                elif(part[0] < 2*0.511):
                    print("Photon is no longer showering")
                    self.shower_state = np.delete(self.shower_state,0)


    def lepton_num(self):
        """Return lepton number from shower
        """
        lepnum = 0
        for part in self.shower_state:
            if abs(part[2] == 11):
                lepnum += part[2]/11
        return lepnum

    def lepton_count(self):
        """Return the total number of electrons and positrons in the shower
        """
        lepcount = 0
        for part in self.shower_state:
            if (part[2] == 11):
                lepcount += 1
        return lepcount
