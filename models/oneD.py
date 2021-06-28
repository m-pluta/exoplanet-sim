from Utility import *


def oneD(plotTitle):
    # Independent Variables
    waterDepth = 4000  # m
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    albedo = c.albedo_Earth
    epsilon = c.epsilonSurface_Earth
    periodFractions = 100
    latitudeWidth = 10  # degrees

    # Initialisation
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    heatCapacity = waterDepth * 1000 * 4200  # J/K/m^2
    L = solarConstant(T_star, R_star, d_planet)  # W/m^2
    t = [0]
    latitudes = []

    for i in range(0, 90, latitudeWidth):
        # Ratio of height of arc (from the view of a cross section of the earth) to the length of the arc
        # i.e Ratio of Flux in vs Flux out
        ratio = (math.sin(math.radians(i + latitudeWidth)) - math.sin(math.radians(i))) / ((latitudeWidth / 360) * 2 * math.pi)
        # Creates a dictionary element for each latitude
        latitudes.append({'lat': (i, i + latitudeWidth), 'tempList': [0.0], 'heatContent': 0, 'albedo': albedo, 'ratio': ratio})

    periods = int(input('Number of periods (15000): '))  # Arbitrary value
    for k in range(periods):
        for i in range(periodFractions):  # For each time step in the given amount of year
            for lat in latitudes:  # Goes through each latitude
                if lat['tempList'][-1] < 273.15:  # If colder than 0*C then higher albedo due to snow cover
                    lat['albedo'] = 0.7
                else:
                    lat['albedo'] = albedo  # If warmer than 0*C then lower albedo due to snow melting
                heat_in = (L * (1 - lat['albedo'])) / 4 * lat['ratio']  # W/m^2
                heat_out = (epsilon * PowerOut(lat['tempList'][-1]))  # W/m^2
                net_heat = heat_in - heat_out
                lat['heatContent'] += net_heat * (period / periodFractions) * c.SiY
                lat['tempList'].append(lat['heatContent'] / heatCapacity)
            t.append(t[-1] + (period / periodFractions))
        print(k)

    # Plotting data
    fig = plt.figure(plotTitle)

    for lat in latitudes:  # Plots temps of each latitude
        plt.plot(t, lat['tempList'], label=str(lat['lat'][0]) + '-' + str(lat['lat'][1]) + '°')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, 0, t[-1])
    fig = addLegend(fig, title='Latitudes: ')

    return fig
