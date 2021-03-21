import matplotlib.pyplot as plt


# functions
def add(a, b):
    return a + b


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

    # Displaying plot
    plt.show()


def zeroD_EBM():
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

    return t, T
