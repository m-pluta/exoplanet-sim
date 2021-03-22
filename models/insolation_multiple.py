import matplotlib.pyplot as plt

from models.insolation_single import *


def insolation_multiple():
    eccentricities = [0, 0.2, 0.4, 0.7]
    colors = ['r', 'g', 'b', 'y']

    fig = plt.figure('Solar insolation on different eccentric orbits')

    for i in range(0, 4):
        t, L = insolation_single(eccentricities[i])
        plt.plot(t, L, c=colors[i], lw=1.25, label=('e = ' + str(eccentricities[i])))
    plt.legend(loc="upper center")

    # Adding labels for title and axes
    fig.suptitle('Light insolation on eccentric orbits (e = 0, 0.1, 0.3, 0.9)', fontsize=12)
    plt.xlabel('time (days)', fontsize=9)
    plt.ylabel('Light Insolation (W/m^2)', fontsize=9)
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig, plt
