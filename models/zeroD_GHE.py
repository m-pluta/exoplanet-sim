from Utility import *


def zeroD_GHE(plotTitle):
    # Independent Variables
    waterDepth = 4000  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilonS = c.epsilonSurface_Earth  # how good of a blackbody the surface of the Earth is
    epsilonA = c.epsilonAtmosphere_Earth  # how good of a blackbody the Atmosphere is
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    periodFractions = 1000  # number of fractions of period

    # Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = PowerOut(T_star)  # Power output of star (Watts/m^2)
    solar_Constant = planetInsolation(Power_output, R_star, d_planet)
    heat_in = (solar_Constant * (1 - albedo)) / 4  # Watts/m^2
    t = [0]
    T = [0]
    net_heat = heat_in

    # Generating data
    heatContent = 0  # J/m^2
    periods = int(input('Number of periods (2000): '))
    for k in range(periods):
        for i in range(periodFractions):
            t.append(t[-1] + period / periodFractions)

            # tempA = ((epsilonS*sigma*T[-1]**4-(1-epsilonA)*epsilonS*sigma*T[-1]**4)/(2*sigma*epsilonA))**0.25
            temp_atmosphere = (0.5 * epsilonS * (T[-1] ** 4)) ** 0.25  # Simplified equation

            heatContent += net_heat * (period / periodFractions) * c.SiY
            T.append(heatContent / heat_capacity)

            # heat_out = (1 - epsilonA) * (epsilonS * c.sigma * T[-1] ** 4) + (epsilonA * c.sigma * temp_atmosphere ** 4)
            heat_out = (1 - epsilonA) * (epsilonS * PowerOut(T[-1])) + (epsilonA * PowerOut(temp_atmosphere))
            net_heat = heat_in - heat_out

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])
    fig = addLegend(fig)

    return fig
