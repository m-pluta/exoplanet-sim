def zeroD_EBM():
    import matplotlib.pyplot as plt
    from Utility import beautifyPlot
    from Utility import plotCelciusLine

    timeStep = 0.2  # (y)
    waterDepth = 4000  # (m)
    L = 1350  # (W / m^2)
    albedo = 0.3  # how much light gets reflected by atmosphere
    epsilon = 0.77  # how good of a blackbody the body is
    sigma = 5.67E-8  # W/m^2 K4
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    heat_in = (L * (1 - albedo)) / 4  # Watts/m^2

    # Init
    t = [0]
    T = [0]

    # Generating Data
    heat_content = heat_capacity * T[0]  # (J / m^2)
    years = 1500
    for i in range(int(years / timeStep)):
        heat_out = epsilon * sigma * pow(T[-1], 4)
        t.append(t[-1] + timeStep)
        heat_content += (heat_in - heat_out) * timeStep * 3.154e7
        T.append(heat_content / heat_capacity)  # (K)

    plotTitle = '0D EBM without Greenhouse effect'
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    fig, plt = beautifyPlot(fig, plt, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig, plt = plotCelciusLine(fig, plt, t[0], t[-1])

    return fig, plt
