import math

import matplotlib.pyplot as plt

from Utility import beautifyPlot, addLegend, plotCelciusLine


def oneD(plotTitle):
    # Declaring Variables
    timeStep = 0.1  # years
    waterDepth = 4000  # m
    L = 1361  # W/m^2
    albedo = 0.3
    epsilonS = 0.7
    sigma = 5.67E-8  # W/m^2/K^4
    heatCapacity = waterDepth * 4.2E6  # J/K/m^2
    latitudeWidth = 10  # degrees
    SiY = 31536000  # Seconds in a year

    # Declaring arrays
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

    years = 24000  # Arbitrary value
    for i in range(1, int(years / timeStep)):  # For each time step in the given amount of year
        for lat in latitudes:  # Goes through each latitude
            if lat['tempList'][-1] < 263.15:  # If colder than -10*C then higher albedo due to snow cover
                lat['albedo'] = 0.7
            else:
                lat['albedo'] = albedo  # If warmer than 10*C then lower albedo due to snow melting
            FluxIn = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
            FluxOut = (epsilonS * sigma * lat['tempList'][-1] ** 4)  # W/m^2
            FluxNet = FluxIn - FluxOut
            lat['heatContent'] += FluxNet * SiY * timeStep
            lat['tempList'].append(lat['heatContent'] / heatCapacity)
        t.append(t[-1] + timeStep)

    # Plotting data
    fig = plt.figure(plotTitle)

    for lat in latitudes:  # Plots temps of each latitude
        plt.plot(t, lat['tempList'], label=str(lat['lat'][0]) + '-' + str(lat['lat'][1]) + '°')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, 0, years)
    fig = addLegend(fig, title='Latitudes: ')

    return fig
