def oneD_GHE():
    import matplotlib.pyplot as plt
    import math

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

    years = 24000  # Arbitrary value
    iceAlbedoThreshold = 223.15
    for i in range(1, int(years / timeStep)):  # For each time step in the given amount of year
        for lat in latitudes:  # Goes through each latitude
            if lat['tempList'][-1] < iceAlbedoThreshold:
                lat['albedo'] = 0.7
            elif iceAlbedoThreshold <= lat['tempList'][-1] <= 273.15:
                # ensures albedo transitions smoothly between 0.7 and 0.3 depending on temperature
                lat['albedo'] = 0.7 - 0.4 * ((lat['tempList'][-1] - iceAlbedoThreshold) / (273.15 - iceAlbedoThreshold))
            else:
                lat['albedo'] = albedo
            tempA = (0.5 * epsilonS * lat['tempList'][-1] ** 4) ** 0.25  # Temp of atmosphere assuming energy balance
            FluxIn = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
            FluxOut = (1 - epsilonA) * epsilonS * sigma * (lat['tempList'][-1] ** 4) + epsilonA * sigma * tempA ** 4
            FluxNet = FluxIn - FluxOut
            lat['heatContent'] += FluxNet * SiY * timeStep
            lat['tempList'].append(lat['heatContent'] / heatCapacity)
        t.append(t[-1] + timeStep)

    print(latitudes[0]['tempList'][-1] - 273.15)

    fig = plt.figure()

    for lat in latitudes:  # Plots temps of each latitude
        plt.plot(t, lat['tempList'], label=str(lat['lat'][0]) + '-' + str(lat['lat'][1]) + '°')
    # Plots line for 0* Celsius
    plt.plot([0, years], [273.15, 273.15], c='c', label='0°C', lw='0.7', linestyle='dashed')

    plt.legend(loc="lower right", title='Latitudes', framealpha=1.0)

    # Adding labels for title and axes
    fig.suptitle('1D EBM with Greenhouse Effect', fontsize=12)
    plt.xlabel('time (years)', fontsize=9)
    plt.ylabel('Surface Temperature (K)', fontsize=9)
    plt.axis([0, 25000, 0, 350])  # Specifying range for axes
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig, plt
