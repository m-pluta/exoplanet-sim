import math

import matplotlib.pyplot as plt

import c
from Utility import beautifyPlot, plotCelciusLine, addLegend, solarConstant


def latitude_stepping_GHE(plotTitle):
    # Independent Variables
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    albedo = c.albedo_Earth
    epsilonS = 0.7
    epsilonA = c.epsilonA_Earth
    timeStep = 1  # years
    waterDepth = 4000  # m
    latitudeWidth = 1  # degrees

    fac = 2  # the factor used to allow <latitudeWidth/fac> increments in latitude

    # Initialisation
    heatCapacity = waterDepth * 4.2E6  # J/K/m^2
    L = solarConstant(R_star, T_star, d_planet)  # W/m^2
    t = [0]
    latitudes = []

    l = []
    T = []

    for i in range(-90 * fac, 90 * fac, latitudeWidth):
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc i.e Ratio of Flux in vs Flux out
        ratio = (math.sin(math.radians((i + latitudeWidth) / fac)) - math.sin(math.radians(i / fac))) / (((latitudeWidth / fac) / 360) * 2 * math.pi)
        # Creates a dictionary element for each latitude
        latitudes.append(
            {'lat': (i / fac, (i + latitudeWidth) / fac), 'tempList': [0.0], 'heatContent': 0, 'albedo': albedo,
             'ratio': ratio})
        l.append(i / fac)

    years = 1000000  # Arbitrary value - the value of this doesnt actually matter too much
    iceAlbedoThreshold = 223.15  # Minimum temp for ice properties to start changing

    for lat in latitudes:
        for i in range(int(years / timeStep)):
            lat['albedo'] = smoothAlbedo(lat['tempList'][-1], iceAlbedoThreshold, 273.15, albedo, 0.7)  # Linear interpolation

            temp_atmosphere = (0.5 * epsilonS * lat['tempList'][-1] ** 4) ** 0.25  # Temp of atmosphere assuming energy balance
            heat_in = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
            heat_out = (1 - epsilonA) * epsilonS * c.sigma * (lat['tempList'][-1] ** 4) + epsilonA * c.sigma * temp_atmosphere ** 4
            net_heat = heat_in - heat_out
            lat['heatContent'] += net_heat * c.SiY * timeStep
            lat['tempList'].append(lat['heatContent'] / heatCapacity)
            if len(lat['tempList']) > 2 and lat['tempList'][-2] != 0:
                if (lat['tempList'][-1] - lat['tempList'][-2]) / lat['tempList'][-2] < 1E-17:  # Check if recent temp has changed a lot since the previous one.
                    T.append(lat['tempList'][-1])
                    if (len(T) % (len(latitudes) / 20) == 0):
                        print(str(round(len(T) / len(latitudes) * 100)) + '%')  # Loading Progress
                    break

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(l, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Latitude (°)', 'Stable Surface Temperature (K)')
    fig = plotCelciusLine(fig, l[0], l[-1])
    fig = addLegend(fig)

    return fig


def smoothAlbedo(currentTemp, iceAlbedoThreshold=263.15, MinAlbedoTemperature=273.15, minAlbedo=0.3, maxAlbedo=0.7):
    if currentTemp < iceAlbedoThreshold:
        return maxAlbedo
    elif iceAlbedoThreshold <= currentTemp <= MinAlbedoTemperature:
        # ensures albedo transitions smoothly between 0.7 and 0.3 depending on temperature - this is basically linear interpolation
        return maxAlbedo - (maxAlbedo - minAlbedo) * (currentTemp - iceAlbedoThreshold) / (MinAlbedoTemperature - iceAlbedoThreshold)
    else:
        return minAlbedo
