import Shower
import matplotlib.pyplot as plt

def part_num_plot(inShower: Shower, plot_name: str):
    shower_itr = 0
    itr_list = [shower_itr]
    lepton_list = [inShower.lepton_count()]
    photon_list = [inShower.photon_count()]

    while (inShower.size() != 0):
        shower_itr += 1
        inShower.propagate()
        itr_list.append(shower_itr)
        lepton_list.append(inShower.lepton_count())
        photon_list.append(inShower.photon_count())
