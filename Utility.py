import math
import os

import matplotlib.pyplot as plt
import numpy as np

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
    if input("Would you like to save this figure? (YES/NO): ").upper() == "YES":

        # Checking which fileName is available next in the directory in order to not overwrite existing plots
        i = 0
        while os.path.exists(f"{fileName}_{i}.png"):
            i += 1

        # Saving plot locally
        print("Saving to " + f"{fileName}_{i}.png")
        fig.savefig(filePath + f"{fileName}_{i}.png", dpi=dpi)
        print("Plot saved to " + f"{fileName}_{i}.png")


def au_to_meters(x):
    return 149597870700 * x


def meters_to_au(x):
    return x / 149597870700


def PowerOut(T_body):
    return c.sigma * T_body ** 4


def planetInsolation(Power_Output, R_star, d_planet):  # This method takes the Power output of the star as the parameter to produce the insolation
    insolation = (4 * math.pi * R_star ** 2 * Power_Output) / (4 * math.pi * d_planet)
    return insolation


def solarConstant(T_star, R_star, d_planet):  # This method takes the Temperature of the star as the parameter to produce the insolation
    insolation = (math.pi * 4 * R_star ** 2 * PowerOut(T_star)) / (4 * math.pi * d_planet ** 2)
    return insolation


# This is an obsolete method
# def generate_heat_in_old(e, periodFractions, d_planet, Power_Output, albedo):
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


def generate_heat_in(ke, periodFractions, d_planet, planetInsolation, albedo):
    heat_in = []
    period = d_planet ** (3 / 2)

    # Generating Heat_in coefficients
    for i in range(0, periodFractions):
        r = ke.radius(i / periodFractions * period)  # Applying Kepler's First Law to find r
        L = planetInsolation / (r / d_planet) ** 2  # Calculating insolation based on distance from star relative to semi major axis
        heat_in.append((L * (1 - albedo)) / 4)

    return heat_in


def generateList(start, end, step):  # from start (inclusive) to end (exclusive)
    e = np.arange(start, end, step).tolist()
    return e


# this is an obsolete method as a more efficient method was found
# def generateEccentricityList(start, end, step):
#     e = [start]
#     while e[-1] < end:
#         e.append(e[-1] + step)
#
#     return e


# No longer in use
def distance_of_planet_to_star(angle, semi_major_axis, e):
    return (semi_major_axis * (1 - e ** 2)) / (1 + e * math.cos(angle))
