from Utility import *


def albedo_temperature(plotTitle):
    T = generateList(250, 300, 0.1)
    A_linear = []
    A_quadratic = []
    for Temp in T:
        A_linear.append(smoothAlbedo_linear(Temp))
        A_quadratic.append(smoothAlbedo_quadratic(Temp))

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(T, A_linear, c='c', linewidth=1.75, linestyle='dashed', label='Linear')
    plt.plot(T, A_quadratic, c='r', linewidth=1.75, label='Quadratic')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Temperature (K)', 'Albedo')
    fig = addLegend(fig, 'upper right', 'Smoothing Types: ')

    return fig
