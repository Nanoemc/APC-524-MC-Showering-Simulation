from Shower.Shower import Shower
from Material.Material_Prop import Material
import matplotlib.pyplot as plt


def part_num_plot(inShower: Shower, plot_name: str):
    shower_itr = 0
    itr_list = [shower_itr]
    lepton_list = [inShower.lepton_count()]
    photon_list = [inShower.photon_count()]

    while inShower.size() != 0:
        shower_itr += 1
        inShower.propagate()
        itr_list.append(shower_itr)
        lepton_list.append(inShower.lepton_count())
        photon_list.append(inShower.photon_count())

    # Make plot
    plt.plot(itr_list, lepton_list, "kv")
    plt.plot(itr_list, photon_list, "r^")
    plt.legend(["Electron/Positrons", "Photons"])
    plt.xlabel("Shower iteration number")
    plt.ylabel("Number of Particles")
    plt.savefig(plot_name)


def energy_disp_plot(inShower: Shower, plot_name: str):
    shower_itr = 0
    itr_list = [shower_itr]
    energy_list = [0]
    while inShower.size() != 0:
        shower_itr += 1
        inShower.propagate()
        itr_list.append(shower_itr)
        energy_list.append(inShower.e_disp)

    # Make plot
    plt.plot(itr_list, energy_list, "r*")
    plt.xlabel("Shower iteration number")
    plt.ylabel("Energy lost due to ionization (MeV)")
    plt.savefig(plot_name)
