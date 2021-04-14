import math

import matplotlib.pyplot as plt

import c
from Utility import beautifyPlot
from Utility import distance_of_planet_to_star
from Utility import plotCelciusLine


def zeroD_e(plotTitle):
    # Independent Variables
    waterDepth = 400  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilon = c.epsilon_Earth  # how good of a blackbody the body is
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    e = float(input("Eccentricity (0.01671): "))  # Eccentricity of planet
    periodFractions = 10000  # number of fractions of period

    # Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    powerOutput = (4 * math.pi * R_star ** 2 * c.sigma * T_star ** 4) / (4 * math.pi * d_planet ** 2)  # Power output of star (Watts)
    t = [0]
    T = [0]
    heat_in = []

    # Generating Heat_in coefficients
    for i in range(1, periodFractions + 1):
        theta = (i / periodFractions) * 2 * math.pi  # Calculating angle in orbit
        r = distance_of_planet_to_star(theta, d_planet, e)  # Applying Kepler's First Law to find r
        L = powerOutput / (r / d_planet) ** 2  # Calculating insolation based on distance from star relative to semi major axis
        heat_in.append((L * (1 - albedo)) / 4)
        print(L)

    # Generating Surface Temperature Data
    heat_content = heat_capacity * T[0]  # (J / m^2)
    years = int(input('Number of years (250): '))
    steps = int(years / (period / periodFractions))

    for i in range(steps):
        t.append(t[-1] + (period / periodFractions))
        heat_out = epsilon * c.sigma * pow(T[-1], 4)

        heat_content += (heat_in[i % periodFractions] - heat_out) * period / periodFractions * c.SiY
        T.append(heat_content / heat_capacity)  # (K)
        # print(t[-1], T[-1])  # For Debugging

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])

    return fig
