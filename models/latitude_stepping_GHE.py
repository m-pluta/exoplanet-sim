import math


def latitude_stepping_GHE():
    # Constants
    timeStep = 1  # years
    waterDepth = 4000  # m
    L = 1361  # W/m^2
    albedo = 0.3
    epsilonS = 0.7
    epsilonA = 0.77
    sigma = 5.67E-8  # W/m^2/K^4
    heatCapacity = waterDepth * 4.2E6  # J/K/m^2
    latitudeWidth = 1  # degrees
    SiY = 31536000  # Seconds in a year

    fac = 2  # the factor used to allow <latitudeWidth/fac> increments in latitude
    t = [0]
    latitudes = []

    l = []
    T = []

    for i in range(-90 * fac, 90 * fac, latitudeWidth):
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc
        # i.e Ratio of Flux in vs Flux out
        ratio = (math.sin(math.radians((i + latitudeWidth) / fac)) - math.sin(math.radians(i / fac))) / (
                ((latitudeWidth / fac) / 360) * 2 * math.pi)
        # Creates a dictionary element for each latitude
        latitudes.append(
            {'lat': (i / fac, (i + latitudeWidth) / fac), 'tempList': [0.0], 'heatContent': 0, 'albedo': albedo,
             'ratio': ratio})
        l.append(i / fac)

    years = 1000000  # Arbitrary value
    iceAlbedoThreshold = 273.15 - 40  # Minimum temp for ice properties to start changing

    for lat in latitudes:
        for i in range(1, int(years / timeStep)):
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
            if len(lat['tempList']) > 2 and lat['tempList'][-2] != 0:
                if (lat['tempList'][-1] - lat['tempList'][-2]) / lat['tempList'][-2] < 1E-17:
                    T.append(lat['tempList'][-1])
                    if (len(T) % (len(latitudes) / 20) == 0):
                        print(str(round(len(T) / len(latitudes) * 100)) + '%')  # Loading Progress
                    break

    return l, T
