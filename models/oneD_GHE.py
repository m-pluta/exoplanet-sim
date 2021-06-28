
from Utility import *


def oneD_GHE(plotTitle):
    # Independent Variables
    waterDepth = 4000  # m
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    albedo = c.albedo_Earth
    epsilonS = c.epsilonSurface_Earth
    epsilonA = c.epsilonAtmosphere_Earth
    periodFractions = 100
    latitudeWidth = 10  # degrees
    StartingTemperature = int(input('Starting Temperature (K): '))  # Arbitrary value

    # Initialisation
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    heatCapacity = waterDepth * 1000 * 4200  # J/K/m^2
    L = solarConstant(T_star, R_star, d_planet)
    t = [0]
    latitudes = []

    for i in range(0, 90, latitudeWidth):
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc i.e Ratio of Flux in vs Flux out
        ratio = (math.sin(math.radians(i + latitudeWidth)) - math.sin(math.radians(i))) / ((latitudeWidth / 360) * 2 * math.pi)

        # Creates a dictionary element for each latitude
        latitudes.append({'lat': (i, i + latitudeWidth), 'tempList': [StartingTemperature], 'heatContent': heatCapacity * StartingTemperature, 'albedo': albedo, 'ratio': ratio})

    periods = int(input('Number of periods (6000): '))  # Arbitrary value
    # iceAlbedoThreshold = float(input('IceAlbedoThreshold (223.15): '))
    for k in range(periods):
        for i in range(periodFractions):  # For each time step in the given amount of year
            for lat in latitudes:  # Goes through each latitude
                # lat['albedo'] = smoothAlbedo_linear(lat['tempList'][-1], iceAlbedoThreshold, 273.15, albedo, 0.7)  # Linear interpolation
                lat['albedo'] = smoothAlbedo_quadratic(lat['tempList'][-1])

                temp_atmosphere = (0.5 * epsilonS * lat['tempList'][-1] ** 4) ** 0.25  # Temp of atmosphere assuming energy balance
                heat_in = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
                heat_out = (1 - epsilonA) * epsilonS * PowerOut(lat['tempList'][-1]) + epsilonA * PowerOut(temp_atmosphere)
                net_heat = heat_in - heat_out
                lat['heatContent'] += net_heat * (period / periodFractions) * c.SiY
                lat['tempList'].append(lat['heatContent'] / heatCapacity)
            t.append(t[-1] + (period / periodFractions))
        print(k)

    fig = plt.figure("1D EBM with Greenhouse Effect")

    for lat in latitudes:  # Plots temps of each latitude
        plt.plot(t, lat['tempList'], label=str(lat['lat'][0]) + '-' + str(lat['lat'][1]) + '°')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, 0, t[-1])
    fig = addLegend(fig, title='Latitudes: ')

    return fig


def smoothAlbedo_linear(currentTemp, iceAlbedoThreshold=263.15, MinAlbedoTemperature=273.15, minAlbedo=0.3, maxAlbedo=0.7):
    if currentTemp < iceAlbedoThreshold:
        return maxAlbedo
    elif iceAlbedoThreshold <= currentTemp <= MinAlbedoTemperature:
        # ensures albedo transitions smoothly between 0.7 and 0.3 depending on temperature - this is basically linear interpolation
        return maxAlbedo - (maxAlbedo - minAlbedo) * (currentTemp - iceAlbedoThreshold) / (MinAlbedoTemperature - iceAlbedoThreshold)
    else:
        return minAlbedo