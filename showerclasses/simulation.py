from math import log
from Material import Material
from Shower import Shower


def simple_shower_alg(inshower : Shower, init_e : float):
    gen = 0
    shower_max = log(init_e/inshower.shower_surface().e_crit())/log(2) #Max depth of shower in radiation lengths (See Tavernier page 193)
    while(inshower.size() != 0):
        inshower.propagate()
        gen += 1
        print(f"x = { gen } radiation length(s)")
        print(f"Shower Size = {inshower.size()}")
        if (gen < shower_max and inshower.lepton_num() != 1):
            print("Unexpected Lepton Number violaiton")

        print("==========================================================================\n\n")




if __name__ == "__main__":
    giant_block_of_polystyrene = Material(100*2000,"") #2 km of fun
    new_shower_1 = Shower(surface = giant_block_of_polystyrene, initial_e = 10000) #10 GeV electron
    new_shower_2 = Shower(surface = giant_block_of_polystyrene, initial_e = 1000000) #1 TeV electron

    simple_shower_alg(new_shower_1,10000)
    simple_shower_alg(new_shower_2,1000000)

