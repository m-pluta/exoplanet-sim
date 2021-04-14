from Utility import addLegend
from models.insolation_single import *


def insolation_multiple(plotTitle):
    eccentricities = [0, 0.2, 0.4, 0.7]
    colors = ['r', 'g', 'b', 'y']

    # Plotting data
    fig = plt.figure(plotTitle)

    for i in range(0, 4):
        t, L = insolation_single('', True, eccentricities[i])
        plt.plot(t, L, c=colors[i], lw=1.25, label=('e = ' + str(eccentricities[i])))

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (days)', 'Light Insolation (W/m^2)')
    fig = addLegend(fig, 'upper center', 'Eccentricities: ')

    return fig
