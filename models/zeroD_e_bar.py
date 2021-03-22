from Utility import distance_of_planet_to_star
def zeroD_e_bar():
    import matplotlib.pyplot as plt
    import math

    waterDepth = 400  # (m)
    albedo = 0.3  # how much light gets reflected by atmosphere
    epsilon = 1  # how good of a blackbody the body is
    sigma = 5.67E-8  # W/m^2 K4
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    SiY = 31557600  # Seconds in a year

    R_star = 0.00465047  # Radius of star (AU)
    d_planet = 1  # Distance of planet from body it is orbiting  (AU)
    T_star = 5778  # Surface Temperature of star (K)
    e = 0  # Eccentricity of planet
    Period_Fractions = 1000  # number of fractions of period

    # Init
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = (4 * math.pi * R_star ** 2 * sigma * T_star ** 4) / (
            4 * math.pi * d_planet ** 2)  # Power output of star (Watts)

    T = [0]
    heat_in = []
    mins = []
    maxs = []
    eccentricities = []

    for j in range(1, 100):  # Iterating through each eccentricity from 0.01 to 0.99
        e += 0.01
        eccentricities.append(e)

        # Generating Heat_in coefficients
        for i in range(1, Period_Fractions + 1):
            theta = (i / Period_Fractions) * 2 * math.pi  # Calculating angle in orbit
            r = distance_of_planet_to_star(theta, d_planet, e)  # Applying Kepler's First Law to find r
            L = Power_output / (
                    r / d_planet) ** 2  # Calculating insolation based on distance from star relative to semi major axis
            heat_in.append((L * (1 - albedo)) / 4)

        # Generating Data
        heat_content = heat_capacity * T[0]  # (J / m^2)
        years = 250
        steps = int(years / (period / Period_Fractions))
        tempMin = 10000
        tempMax = 0

        for i in range(steps):
            heat_out = epsilon * sigma * pow(T[-1], 4)

            heat_content += (heat_in[i % Period_Fractions] - heat_out) * period / Period_Fractions * SiY
            T.append(heat_content / heat_capacity)  # (K)
            # print(t[-1], T[-1])  # For Debugging
            if i > 240 / (period / Period_Fractions):
                if T[-1] < tempMin:
                    tempMin = T[-1]  # keeping track of the max and min temperatures for each eccentricity

                if T[-1] > tempMax:
                    tempMax = T[-1]

        mins.append(tempMin)
        maxs.append(tempMax)
        tempMin = 10000
        tempMax = 0
        T = [0]  # Reset certain temporary variable for next eccentricity iteration
        heat_in = []
        print(str(round(e, 2)))

    fig = plt.figure()

    tempE = 0
    for i in range(0, 99):
        tempE += 0.01

        # Height minimum
        minHeight = 5
        height = round(maxs[i] - mins[i], 3)
        if height < minHeight:
            height = minHeight

        barWidth = 0.006  # Set to 0.006 for default or 0.01 for connected bars

        plt.bar(round(tempE, 2), height, width=barWidth, bottom=round(mins[i], 3), align='center',
                color='c')

        # print(str(round(tempE, 2)) + " - " + str(round(maxs[i] - mins[i], 3)))

    # Plots line for 0* Celsius
    plt.plot([0, 1], [273.15, 273.15], c='r', label='0°C', lw='0.5', linestyle='dashed')

    plt.legend(loc="lower right", title='Extra lines:', framealpha=1.0)

    # Adding labels for title and axes
    fig.suptitle('0D EBM with eccentricity variation', fontsize=12)
    plt.xlabel('Eccentricity (0.01-0.99)', fontsize=9)
    plt.ylabel('Mean Surface temperature (K)', fontsize=9)
    plt.axis([-0.05, 1.05, 200, 2700])
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)

    return fig, plt
