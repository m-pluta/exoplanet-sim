import math

import matplotlib.pyplot as plt


def oneD():
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

    # Temperature at 0-10* in Celsius (for testing)

    fig = plt.figure()

    for lat in latitudes:  # Plots temps of each latitude
        plt.plot(t, lat['tempList'], label=str(lat['lat'][0]) + '-' + str(lat['lat'][1]) + '°')

    # Plots line for 0* Celsius
    plt.plot([0, years], [273.15, 273.15], c='c', label='0°C', lw='1.25', linestyle='dashed')

    plt.legend(loc="lower right", title='Latitudes', framealpha=1.0)

    # Adding labels for title and axes
    fig.suptitle('1D EBM without Greenhouse Effect', fontsize=12)
    plt.xlabel('time (years)', fontsize=9)
    plt.ylabel('Surface Temperature (K)', fontsize=9)
    plt.axis([0, 25000, 0, 350])  # Specifying range for axes
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig, plt
