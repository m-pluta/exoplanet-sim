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
#     plt.annotate(str(round(T[-1], 3)), (t[-1], T[-1]), xycoords='data', xytext=(t[-1] - 125, T[-1] - 20))
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
    fig.suptitle(Title, fontsize=14)
    plt.xlabel(x_axis, fontsize=10)
    plt.ylabel(y_axis, fontsize=10)
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig


def plotCelciusLine(fig, t1, t2):
    plt.plot([t1, t2], [273.15, 273.15], c='c', label='0°C', lw='1.25', linestyle='dashed')
    plt.legend(loc="lower right", title='Extra lines:', framealpha=1.0)
    return fig


def addLegend(fig, pos='lower right', title='Extra Lines: '):
    plt.legend(loc=pos, title=title, framealpha=1.0)
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


def solarConstant(R_star, T_star, d_planet):
    return (4 * math.pi * R_star ** 2 * c.sigma * T_star ** 4) / (4 * math.pi * d_planet ** 2)


# This is an obsolete method
# def generate_heat_in(e, periodFractions, d_planet, Power_Output, albedo):
#     heat_in = []
#
#     # Generating Heat_in coefficients
#     for i in range(0, periodFractions):
#         theta = (i / periodFractions) * 2 * math.pi  # Calculating angle in orbit
#         r = distance_of_planet_to_star(theta, d_planet, e)  # Applying Kepler's First Law to find r
#         L = Power_Output / (r / d_planet) ** 2  # Calculating insolation based on distance from star relative to semi major axis
#         heat_in.append((L * (1 - albedo)) / 4)
#
#     return heat_in


def generate_heat_in_updated(ke, periodFractions, d_planet, Power_Output, albedo):
    heat_in = []
    period = d_planet ** (3 / 2)

    # Generating Heat_in coefficients
    for i in range(0, periodFractions):
        r = ke.radius(i / periodFractions * period)  # Applying Kepler's First Law to find r
        L = Power_Output / (r / d_planet) ** 2  # Calculating insolation based on distance from star relative to semi major axis
        heat_in.append((L * (1 - albedo)) / 4)

    return heat_in


def generateEccentricityList(start, end, step):
    e = [start]
    while e[-1] < end:
        e.append(e[-1] + step)

    return e


# No longer in use
def distance_of_planet_to_star(angle, semi_major_axis, e):
    return (semi_major_axis * (1 - e ** 2)) / (1 + e * math.cos(angle))
