import math

import matplotlib.pyplot as plt

from Utility import beautifyPlot, plotCelciusLine, addLegend


def oneD_GHE(plotTitle):
    # Constants
    timeStep = 0.1  # years
    waterDepth = 4000  # m
    L = 1361  # W/m^2
    albedo = 0.3
    epsilonS = 0.7
    epsilonA = 0.77
    sigma = 5.67E-8  # W/m^2/K^4
    heatCapacity = waterDepth * 4.2E6  # J/K/m^2
    latitudeWidth = 10  # degrees
    SiY = 31536000  # Seconds in a year

    t = [0]
    latitudes = []
    for i in range(0, 90, latitudeWidth):
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc
        # i.e Ratio of Flux in vs Flux out
        ratio = (math.sin(math.radians(i + latitudeWidth)) - math.sin(math.radians(i))) / (
                (latitudeWidth / 360) * 2 * math.pi)
        # Creates a dictionary element for each latitude
        latitudes.append(
            {'lat': (i, i + latitudeWidth), 'tempList': [0.0], 'heatContent': 0, 'albedo': albedo, 'ratio': ratio})

    years = int(input('Number of years (24000): '))  # Arbitrary value
    iceAlbedoThreshold = int(input('IceAlbedoThreshold (223.15): '))

    for i in range(int(years / timeStep)):  # For each time step in the given amount of year
        for lat in latitudes:  # Goes through each latitude
            lat['albedo'] = smoothAlbedo(lat['tempList'][-1], iceAlbedoThreshold, 273.15, albedo, 0.7)  # Linear interpolation

            temp_atmosphere = (0.5 * epsilonS * lat['tempList'][-1] ** 4) ** 0.25  # Temp of atmosphere assuming energy balance
            FluxIn = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
            FluxOut = (1 - epsilonA) * epsilonS * sigma * (lat['tempList'][-1] ** 4) + epsilonA * sigma * temp_atmosphere ** 4
            FluxNet = FluxIn - FluxOut
            lat['heatContent'] += FluxNet * SiY * timeStep
            lat['tempList'].append(lat['heatContent'] / heatCapacity)
        t.append(t[-1] + timeStep)

    fig = plt.figure("1D EBM with Greenhouse Effect")

    for lat in latitudes:  # Plots temps of each latitude
        plt.plot(t, lat['tempList'], label=str(lat['lat'][0]) + '-' + str(lat['lat'][1]) + '°')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, 0, years)
    fig = addLegend(fig, title='Latitudes: ')

    return fig


def smoothAlbedo(currentTemp, iceAlbedoThreshold=263.15, MinAlbedoTemperature=273.15, minAlbedo=0.3, maxAlbedo=0.7):
    if currentTemp < iceAlbedoThreshold:
        return maxAlbedo
    elif iceAlbedoThreshold <= currentTemp <= MinAlbedoTemperature:
        # ensures albedo transitions smoothly between 0.7 and 0.3 depending on temperature - this is basically linear interpolation
        return maxAlbedo - (maxAlbedo - minAlbedo) * (currentTemp - iceAlbedoThreshold) / (MinAlbedoTemperature - iceAlbedoThreshold)
    else:
        return minAlbedo
