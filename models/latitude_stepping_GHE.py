from Utility import *


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
    heatCapacity = waterDepth * 1000 * 4200  # J/K/m^2
    L = solarConstant(T_star, R_star, d_planet)  # W/m^2
    latitudeData = []

    latitudes = generateList(-90, 90, latitudeWidth)
    T = []

    # factor = 1  # the factor used to allow <latitudeWidth/fac> increments in latitude
    # magnitude = math.floor(math.log10(latitudeWidth))
    # if magnitude < 0:  # Finds magnitude of latitudeWidth and scales for loop parameters so they are all integers depending on the magnitude
    #     factor = math.pow(10, abs(magnitude))

    for l in latitudes:
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc i.e Ratio of Flux in vs Flux out
        # ratio = math.sin(math.radians(abs(l) + abs(latitudeWidth))) - math.sin(math.radians(abs(l))) / ((latitudeWidth / 360) * 2 * math.pi)
        ratio = abs(math.sin(math.radians(abs(l + 1))) - math.sin(math.radians(abs(l)))) / ((latitudeWidth / 360) * 2 * math.pi)
        # Creates a dictionary element for each latitude
        latitudeData.append({'lat': (l, (l + latitudeWidth)), 'tempList': [StartingTemperature], 'heatContent': StartingTemperature * heatCapacity, 'albedo': albedo, 'ratio': ratio})
        print(latitudeData[-1])

    periods = 10000  # Arbitrary value

    for lat in latitudeData:
        addedTemp = False
        for i in range(periods * periodFractions):
            lat['albedo'] = smoothAlbedo_quadratic(lat['tempList'][-1])  # Linear interpolation

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
    plt.plot(latitudes, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Latitude (°)', 'Stable Surface Temperature (K)')
    fig = plotCelciusLine(fig, latitudes[0], latitudes[-1])
    fig = addLegend(fig)

    return fig
