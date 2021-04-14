import math

import matplotlib.pyplot as plt

import c
from Utility import beautifyPlot, solarConstant
from Utility import distance_of_planet_to_star


#  Sources: Kepler's First Law: https://www.vanderbilt.edu/AnS/physics/astrocourses/ast201/keplerslaws_1.html
#                               http://astronomy.nmsu.edu/nicole/teaching/ASTR505/lectures/lecture08/slide13.html#:~:text=The%20squares%20of%20the%20sidereal,square%20of%20its%20sidereal%20period.

def insolation_single(plotTitle):
    # Independent Variables
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # (K)
    periodFractions = 1000  # fraction of period acts as timeStep
    e = float(input("Eccentricity: "))

    # Initialisation
    period = math.pow(d_planet, 1.5) * 365.25
    Power_output = solarConstant(R_star, T_star, d_planet)

    t = []
    L = []

    # Generating Data
    for i in range(0, periodFractions):
        t.append((i / periodFractions) * period)
        theta = (i / periodFractions) * 2 * math.pi  # Calculating angle in orbit
        r = distance_of_planet_to_star(theta, d_planet, e)  # Applying Kepler's First Law to find r
        newL = Power_output / (r / d_planet) ** 2  # Calculating insolation based on position in orbit relative to the starting point
        L.append(newL)

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, L, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle + ' (e=' + str(e) + ')', 'time (days)', 'Light Insolation (W/m^2)')

    return fig
