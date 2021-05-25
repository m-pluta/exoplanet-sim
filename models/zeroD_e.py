import math

import matplotlib.pyplot as plt
from PyAstronomy import pyasl

import c
from Utility import addLegend
from Utility import beautifyPlot
from Utility import generate_heat_in_updated
from Utility import plotCelciusLine
from Utility import solarConstant


def zeroD_e(plotTitle):
    # Independent Variables
    waterDepth = 400  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilon = c.epsilonA_Earth  # how good of a blackbody the body is
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    e = float(input("Eccentricity (0.01671): "))  # Eccentricity of planet
    periodFractions = 1000  # number of fractions of period

    # Initialisationss
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = solarConstant(R_star, T_star, c.d_Earth)  # Power output of star (Watts)
    t = [0]
    T = [0]

    ke = pyasl.KeplerEllipse(d_planet, period, e, Omega=0., i=0.0, w=0.0)
    heat_in = generate_heat_in_updated(ke, periodFractions, d_planet, Power_output, albedo)
    # heat_in = generate_heat_in(e, periodFractions, d_planet, Power_output, albedo)
    # print(*heat_in, sep="\n")

    # Generating Surface Temperature Data
    heat_content = heat_capacity * T[0]  # (J / m^2)
    years = int(input('Number of years (250): '))
    steps = int(years / (period / periodFractions))

    for i in range(steps):
        t.append(t[-1] + (period / periodFractions))
        heat_out = epsilon * c.sigma * pow(T[-1], 4)

        heat_content += (heat_in[i % periodFractions] - heat_out) * period / periodFractions * c.SiY
        T.append(heat_content / heat_capacity)  # (K)

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])
    fig = addLegend(fig)

    return fig
