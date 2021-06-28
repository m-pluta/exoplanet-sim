import math

import matplotlib.pyplot as plt

import c
from Utility import beautifyPlot, plotCelciusLine, addLegend, solarConstant


def latitude_stepping_GHE(plotTitle):
    # Independent Variables
    waterDepth = 4000  # m
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    albedo = c.albedo_Earth
    epsilonS = c.epsilonSurface_Earth
    epsilonA = c.epsilonAtmosphere_Earth
    periodFractions = 1
    latitudeWidth = 1  # degrees
    StartingTemperature = int(input('Starting Temperature (K): '))  # Arbitrary value

    # Initialisation
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    heatCapacity = waterDepth * 4.2E6  # J/K/m^2
    L = solarConstant(T_star, R_star, d_planet)  # W/m^2
    latitudes = []

    l = []
    T = []

    factor = 1  # the factor used to allow <latitudeWidth/fac> increments in latitude
    magnitude = math.floor(math.log10(latitudeWidth))
    if magnitude < 0:  # Finds magnitude of latitudeWidth and scales for loop parameters so they are all integers depending on the magnitude
        factor = math.pow(10, abs(magnitude))

    for i in range(int(-90 * factor), int(90 * factor), int(latitudeWidth * factor)):
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc i.e Ratio of Flux in vs Flux out
        ratio = (math.sin(math.radians((i + latitudeWidth) / factor)) - math.sin(math.radians(i / factor))) / (((latitudeWidth / factor) / 360) * 2 * math.pi)
        # Creates a dictionary element for each latitude
        latitudes.append(
            {'lat': (i / factor, (i + latitudeWidth) / factor), 'tempList': [StartingTemperature], 'heatContent': StartingTemperature * heatCapacity, 'albedo': albedo,
             'ratio': ratio})
        l.append(i / factor)

    periods = 10000  # Arbitrary value - the value of this doesnt actually matter too much

    for lat in latitudes:
        addedTemp = False
        for i in range(periods * periodFractions):
            lat['albedo'] = smoothAlbedo_linear(lat['tempList'][-1])  # Linear interpolation

            temp_atmosphere = (0.5 * epsilonS * lat['tempList'][-1] ** 4) ** 0.25  # Temp of atmosphere assuming energy balance
            heat_in = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
            heat_out = (1 - epsilonA) * epsilonS * c.sigma * (lat['tempList'][-1] ** 4) + epsilonA * c.sigma * temp_atmosphere ** 4
            net_heat = heat_in - heat_out
            lat['heatContent'] += net_heat * (period / periodFractions) * c.SiY
            lat['tempList'].append(lat['heatContent'] / heatCapacity)
            if len(lat['tempList']) > 2 and lat['tempList'][-2] != 0:
                if (lat['tempList'][-1] - lat['tempList'][-2]) / lat['tempList'][-2] < 1E-20:  # Check if recent temp has changed a lot since the previous one.
                    T.append(lat['tempList'][-1])
                    addedTemp = True
                    break
        if not addedTemp:
            T.append(lat['tempList'][-1])
        print(lat['lat'])

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(l, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Latitude (°)', 'Stable Surface Temperature (K)')
    fig = plotCelciusLine(fig, l[0], l[-1])
    fig = addLegend(fig)

    return fig


def smoothAlbedo_linear(currentTemp, iceAlbedoThreshold=223.15, MinAlbedoTemperature=273.15, minAlbedo=0.3, maxAlbedo=0.7):
    if currentTemp < iceAlbedoThreshold:
        return maxAlbedo
    elif iceAlbedoThreshold <= currentTemp <= MinAlbedoTemperature:
        # ensures albedo transitions smoothly between 0.7 and 0.3 depending on temperature - this is basically linear interpolation
        return maxAlbedo - (maxAlbedo - minAlbedo) * (currentTemp - iceAlbedoThreshold) / (MinAlbedoTemperature - iceAlbedoThreshold)
    else:
        return minAlbedo


def smoothAlbedo_quadratic(Temp, T_i=260, T_o=293, alpha_o=0.289, alpha_i=0.7):
    if Temp <= T_i:
        return alpha_i
    elif T_i < Temp < T_o:
        return alpha_o + (alpha_i - alpha_o) * ((Temp - T_o) ** 2) / ((T_i - T_o) ** 2)
    else:
        return alpha_o
