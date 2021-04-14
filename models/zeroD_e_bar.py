import math

import matplotlib.pyplot as plt

import c
from Utility import addLegend
from Utility import beautifyPlot
from Utility import generateEccentricityList
from Utility import generate_heat_in
from Utility import plotCelciusLine
from Utility import solarConstant


def zeroD_e_bar(plotTitle):
    # Independent Variables
    waterDepth = 400  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilon = c.epsilonA_Earth  # how good of a blackbody the body is

    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = 5778  # Surface Temperature of star (K)
    periodFractions = 1000  # number of fractions of period

    # Global Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = solarConstant(R_star, T_star, d_planet)  # incidentPower from star (W)

    eccentricities = generateEccentricityList(0.5, 0.99, 0.01)
    mins = []
    maxs = []

    for e in eccentricities:  # Iterating through each eccentricity from 0.01 to 0.99

        # Initialisation
        T = [0]
        heat_content = heat_capacity * T[0]  # (J / m^2)
        years = 250
        steps = int(years / (period / periodFractions))
        tempMin = 1E24
        heat_in = generate_heat_in(e, periodFractions, d_planet, Power_output, albedo)

        for i in range(steps):
            heat_out = epsilon * c.sigma * pow(T[-1], 4)

            heat_content += (heat_in[i % periodFractions] - heat_out) * period / periodFractions * c.SiY
            T.append(heat_content / heat_capacity)  # (K)
            if i > (years - 10 * period) / (period / periodFractions):  # Only keeps track of minimum temperatures for the last 10 periods in EBM
                if T[-1] < tempMin:
                    tempMin = T[-1]  # keeping track of the minimum temperature

        mins.append(tempMin)
        maxs.append(max(T))

    # Plotting data
    fig = plt.figure(plotTitle)

    tempE = 0
    for i in range(0, len(eccentricities)):
        # Height minimum
        minBarHeight = 5
        height = round(maxs[i] - mins[i], 3)
        if height < minBarHeight:
            height = minBarHeight

        barWidth = 0.006  # Set to 0.006 for default or 0.01 for connected bars
        plt.bar(round(eccentricities[i], 2), height, width=barWidth, bottom=round(mins[i], 3), align='center', color='r')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Eccentricity', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, min(eccentricities), max(eccentricities))
    fig = addLegend(fig, 'upper left', 'Plots: ')

    return fig
