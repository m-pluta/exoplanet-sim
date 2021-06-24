from Utility import *


def zeroD_EBM(plotTitle):
    # Independent Variables
    waterDepth = 4000  # (m)
    albedo = c.albedo_Earth  # how much light gets reflected by atmosphere
    epsilon = c.epsilonSurface_Earth  # how good of a blackbody the body is
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth * 4  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # Surface Temperature of star (K)
    periodFractions = 1000  # number of fractions of period

    # Initialisation
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = PowerOutput(T_star)  # Power output of star (Watts/m^2)
    solar_Constant = planetInsolation(Power_output, R_star, d_planet)
    heat_in = (solar_Constant * (1 - albedo)) / 4  # Watts/m^2
    t = [0]
    T = [0]

    # Generating Data
    heat_content = heat_capacity * T[0]  # (J / m^2)
    periods = int(input('Number of periods (1000): '))
    for i in range(periods):
        for j in range(periodFractions):
            t.append(t[-1] + period / periodFractions)
            heat_out = epsilon * c.sigma * T[-1] ** 4
            heat_content += (heat_in - heat_out) * (period / periodFractions) * c.SiY
            T.append(heat_content / heat_capacity)  # (K)

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])
    fig = addLegend(fig)

    return fig
