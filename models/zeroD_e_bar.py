from PyAstronomy import pyasl

from Utility import *


def zeroD_e_bar(plotTitle):
    # Independent Variables
    waterDepth = 4000  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere (0-1)
    epsilon = c.epsilonSurface_Earth  # how good of a blackbody the body is (0-1)
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    periodFractions = 365  # number of fractions of period

    # Global Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_Output = PowerOut(T_star)  # Power irradiated from the star's surface (W/m^2)
    solar_Constant = planetInsolation(Power_Output, R_star, d_planet)  # Insolation incident on the planet's surface (W/m^2)
    eccentricities = generateList(0, 0.95, 0.01)  # List containing all the eccentricities being plotted
    minTemps = []
    maxTemps = []

    for e in eccentricities:  # Iterating through each eccentricity from 0.01 to 0.99

        # Initialisation
        T = [0]
        heat_content = heat_capacity * T[0]  # (J / m^2)
        periods = 1000
        tempMin = 1E24
        ke = pyasl.KeplerEllipse(d_planet, period, e, Omega=0., i=0.0, w=0.0)
        heat_in = generate_heat_in(ke, periodFractions, d_planet, solar_Constant, albedo)
        for k in range(periods):
            for i in range(periodFractions):
                heat_out = epsilon * PowerOut(T[-1])

                heat_content += (heat_in[i] - heat_out) * (period / periodFractions * c.SiY)
                T.append(heat_content / heat_capacity)  # (K)
                if periods - k < 20:  # Only keeps track of minimum temperatures for the last 20 periods in EBM
                    if T[-1] < tempMin:
                        tempMin = T[-1]  # Keeping track of the minimum temperature
        print(str(round(e, 2)))
        minTemps.append(tempMin)
        maxTemps.append(max(T))

    # Plotting data
    fig = plt.figure(plotTitle)

    for i in range(len(eccentricities)):
        # Height minimum
        minBarHeight = 2
        height = round(maxTemps[i] - minTemps[i], 3)
        if height < minBarHeight:
            height = minBarHeight

        barWidth = 0.006  # Set to 0.006 for default or 0.01 for connected bars
        plt.bar(round(eccentricities[i], 2), height, width=barWidth, bottom=round(minTemps[i], 3), align='center', color='r')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Eccentricity', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, min(eccentricities), max(eccentricities))
    fig = addLegend(fig, 'upper left', 'Plots: ')

    return fig
