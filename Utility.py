import math

import matplotlib.pyplot as plt

import c


# def plotGraph(t, T, Title, x_axis, y_axis, celciusLine):
#     fig = plt.figure(Title)
#     plt.plot(t, T, c='r', linewidth=1.75)
#
#     if celciusLine == 'true':
#         plt.plot([t[0], t[-1]], [273.15, 273.15], c='c', label='0°C', lw='1.25', linestyle='dashed')
#
#         plt.legend(loc="lower right", title='Extra lines:', framealpha=1.0)
#
#     # Adding labels for title and axes
#     fig.suptitle(Title, fontsize=12)
#     plt.xlabel(x_axis, fontsize=9)
#     plt.ylabel(y_axis, fontsize=9)
#     plt.minorticks_on()  # minor ticks
#
#     # Drawing major & minor gridlines
#     plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
#     plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)
#
#     return fig, plt


def beautifyPlot(fig, Title, x_axis, y_axis):
    # Adding labels for title and axes
    fig.suptitle(Title, fontsize=12)
    plt.xlabel(x_axis, fontsize=9)
    plt.ylabel(y_axis, fontsize=9)
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig


def plotCelciusLine(fig, t1, t2):
    plt.plot([t1, t2], [273.15, 273.15], c='c', label='0°C', lw='1.25', linestyle='dashed')
    plt.legend(loc="lower right", title='Extra lines:', framealpha=1.0)
    return fig


def savePlot(fig, filePath, fileName, dpi=1000):
    if input("Would you like to save this figure? (YES/NO): ") == "YES":
        # Saving plot locally
        print('Saving to ' + fileName + '.png')
        fig.savefig(filePath + fileName + '.png', dpi=dpi)
        print('Plot saved to ' + fileName + '.png')


def au_to_meters(x):
    return 149597870700 * x


def meters_to_au(x):
    return x / 149597870700


def solarOutput(R_star, T_star, d_planet):
    return (4 * math.pi * R_star ** 2 * c.sigma * T_star ** 4) / (4 * math.pi * d_planet ** 2)


def distance_of_planet_to_star(angle, semi_major_axis, e):
    return (semi_major_axis * (1 - e ** 2)) / (1 + e * math.cos(angle))
