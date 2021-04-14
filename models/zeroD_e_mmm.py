import math

import matplotlib.pyplot as plt

import c
from Utility import addLegend
from Utility import beautifyPlot
from Utility import generateEccentricityList
from Utility import generate_heat_in
from Utility import plotCelciusLine
from Utility import solarOutput


def zeroD_e_mmm(plotTitle):
    # Independent Variables
    waterDepth = 400  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilon = c.epsilon_Earth  # how good of a blackbody the body is

    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = 5778  # Surface Temperature of star (K)
    periodFractions = 1000  # number of fractions of period

    # Global Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = solarOutput(R_star, T_star, d_planet)  # incidentPower from star (W)

    eccentricities = generateEccentricityList(0.5, 0.99, 0.01)
    mins = []
    means = []
    maxs = []

    for e in eccentricities:  # Iterating through each eccentricity from 0.01 to 0.99

        # Initialisation
        T = [0]
        heat_content = heat_capacity * T[0]  # (J / m^2)
        years = 250
        steps = int(years / (period / periodFractions))
        tempMin = 1E24
        heat_in = generate_heat_in(e, periodFractions, d_planet, Power_output, albedo)

        tempMax = 0
        tempMean = 0
        countMean = 0

        for i in range(steps):
            heat_out = epsilon * c.sigma * pow(T[-1], 4)

            heat_content += (heat_in[i % periodFractions] - heat_out) * period / periodFractions * c.SiY
            T.append(heat_content / heat_capacity)  # (K)

            if i > (years - 10 * period) / (period / periodFractions):  # Only keeps track of minimum temperatures for the last 10 periods in EBM
                if T[-1] < tempMin:
                    tempMin = T[-1]  # keeping track of the minimum temperature

                tempMean += T[-1]
                countMean += 1

        mins.append(tempMin)
        maxs.append(max(T))
        means.append(tempMean / countMean)

        print(str(round(e, 2) * 100))

    # Plotting data
    fig = plt.figure(plotTitle)

    plt.plot(eccentricities, mins, c='r', linewidth=0.75, label='Minimum')
    plt.plot(eccentricities, means, c='g', linewidth=0.75, label="Mean")
    plt.plot(eccentricities, maxs, c='b', linewidth=0.75, label='Maximum')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Eccentricity', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, min(eccentricities), max(eccentricities))
    fig = addLegend(fig, 'upper left', 'Plots: ')

    return fig
