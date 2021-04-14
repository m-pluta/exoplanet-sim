from Utility import addLegend
from models.insolation_single import *


def insolation_multiple(plotTitle):
    eccentricities = [(0, 'c'), (0.2, 'g'), (0.4, 'b'), (0.6, 'y'), (0.8, 'm')]

    # Plotting data
    fig = plt.figure(plotTitle)

    for i in range(0, len(eccentricities)):
        t, L = insolation_single('', True, eccentricities[i][0])
        plt.plot(t, L, c=eccentricities[i][1], lw=1.25, label=('e = ' + str(eccentricities[i][0])))

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (days)', 'Light Insolation (W/m^2)')
    fig = addLegend(fig, 'upper center', 'Eccentricities: ')

    return fig
