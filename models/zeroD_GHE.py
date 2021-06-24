import matplotlib.pyplot as plt

import c
from Utility import addLegend
from Utility import beautifyPlot
from Utility import plotCelciusLine
from Utility import solarConstant


def zeroD_GHE(plotTitle):
    # Independent Variables
    timeStep = 0.1  # years
    waterDepth = 4000  # metres
    L = solarConstant(c.T_Sun, c.R_Sun, c.d_Earth)
    albedo = c.albedo_Earth
    epsilonS = c.epsilonSurface_Earth
    epsilonA = c.epsilonAtmosphere_Earth

    # Declaring variables and initialisation
    heatCapacity = waterDepth * 4.2E6  # JK/m^2
    heat_in = L * (1 - albedo) / 4  # W/m^2
    t = [0]
    T = [0]  # K
    net_heat = heat_in

    heatContent = 0  # J/m^2
    years = int(input('Number of years (1500): '))
    for i in range(int(years / timeStep)):
        # tempA = ((epsilonS*sigma*T[-1]**4-(1-epsilonA)*epsilonS*sigma*T[-1]**4)/(2*sigma*epsilonA))**0.25
        temp_atmosphere = (0.5 * epsilonS * (T[-1] ** 4)) ** 0.25  # Simplified equation

        heatContent += net_heat * c.SiY * timeStep
        T.append(heatContent / heatCapacity)

        heat_out = (1 - epsilonA) * (epsilonS * c.sigma * T[-1] ** 4) + (epsilonA * c.sigma * temp_atmosphere ** 4)
        net_heat = heat_in - heat_out

        t.append(t[-1] + timeStep)

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])
    fig = addLegend(fig)

    return fig
