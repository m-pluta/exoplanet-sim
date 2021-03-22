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

    for j in range(1, 100):  # Iterating through each eccentricity from 0.01 to 0.9
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
        plt.plot([round(tempE, 2), round(tempE, 2)], [round(mins[i], 3), round(maxs[i], 3)], c='c',
                 lw='2', )  # Displaying a bar for each eccentricity showing the variation in temperature
        print(str(round(tempE, 2)) + " - " + str(round(maxs[i] - mins[i], 3)))
    return fig, plt
