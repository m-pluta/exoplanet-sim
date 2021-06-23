import matplotlib.pyplot as plt

import c
from Utility import addLegend
from Utility import beautifyPlot
from Utility import plotCelciusLine
from Utility import solarConstant


def zeroD_EBM(plotTitle):
    # Independent variables
    timeStep = 0.2  # (y)
    waterDepth = 4000  # (m)
    L = solarConstant(c.T_Sun, c.R_Sun, c.d_Earth)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilon = c.epsilonA_Earth  # how good of a blackbody the body is

    # Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    heat_in = (L * (1 - albedo)) / 4  # Watts/m^2
    t = [0]
    T = [0]

    # Generating Data
    heat_content = heat_capacity * T[0]  # (J / m^2)
    years = int(input('Number of years (1500): '))
    for i in range(int(years / timeStep)):
        heat_out = epsilon * c.sigma * pow(T[-1], 4)
        t.append(t[-1] + timeStep)
        heat_content += (heat_in - heat_out) * timeStep * c.SiY
        T.append(heat_content / heat_capacity)  # (K)

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])
    fig = addLegend(fig)

    return fig
