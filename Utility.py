import matplotlib.pyplot as plt

# Constants
SiY = 31556952


# functions
def add(a, b):
    return a + b


def zeroD_EBM():
    timeStep = 0.2  # (y)
    waterDepth = 4000  # (m)
    L = 1350  # (W / m^2)
    albedo = 0.3  # how much light gets reflected by atmosphere
    epsilon = 1  # how good of a blackbody the body is
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

    fig = plt.figure()
    plt.plot(t, T, c='r', linewidth=2.25)
    # Plots line for 0* Celsius
    plt.plot([0, years], [273.15, 273.15], c='c', label='0°C', lw='0.7', linestyle='dashed')

    plt.legend(loc="lower right", title='Extra lines:', framealpha=1.0)

    # Adding labels for title and axes
    fig.suptitle('0D EBM without Greenhouse effect', fontsize=12)
    plt.xlabel('time (years)', fontsize=9)
    plt.ylabel('Surface temperature (K)', fontsize=9)
    plt.axis([0, 1600, 0, 300])  # Specifying range for axes
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    # Saving plot locally
    iName = '0D EBM without GHE'
    dpi = 500
    print('Saving to ' + iName + '.png')
    fig.savefig('C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\' + iName + '.png', dpi=dpi)
    print('Plot saved to ' + iName + '.png')
    print('Saving to ' + iName + '_2x.png')
    fig.savefig('C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\' + iName + '_2x.png', dpi=(2 * dpi))
    print('Plot saved to ' + iName + '_2x.png')

    # Displaying plot
    plt.show()
