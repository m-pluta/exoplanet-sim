import math

import matplotlib.pyplot as plt


def plotGraph(t, T, Title, x_axis, y_axis, celciusLine):
    fig = plt.figure()
    plt.plot(t, T, c='r', linewidth=2.25)

    if celciusLine == 'true':
        plt.plot([t[0], t[-1]], [273.15, 273.15], c='c', label='0°C', lw='0.7', linestyle='dashed')

        plt.legend(loc="lower right", title='Extra lines:', framealpha=1.0)

    # Adding labels for title and axes
    fig.suptitle(Title, fontsize=12)
    plt.xlabel(x_axis, fontsize=9)
    plt.ylabel(y_axis, fontsize=9)
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig, plt


def savePlot(fig, filePath, fileName, dpi=1000):
    # Saving plot locally
    print('Saving to ' + fileName + '.png')
    fig.savefig(filePath + fileName + '.png', dpi=dpi)
    print('Plot saved to ' + fileName + '_2x.png')


def au_to_meters(x):
    return 149597870700 * x


def meters_to_au(x):
    return x / 149597870700


def distance_of_planet_to_star(angle, R_planet, e):
    return (R_planet * (1 - e ** 2)) / (1 + e * math.cos(angle))
