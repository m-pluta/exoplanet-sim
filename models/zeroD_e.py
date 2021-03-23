import math

from Utility import distance_of_planet_to_star


def zeroD_e(inputE=0.01671):
    waterDepth = 400  # (m)
    albedo = 0.3  # how much light gets reflected by atmosphere
    epsilon = 0.77  # how good of a blackbody the body is
    sigma = 5.67E-8  # W/m^2 K4
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    SiY = 31557600  # Seconds in a year

    R_star = 0.00465047  # Radius of star (AU)
    d_planet = 1  # Distance of planet from body it is orbiting  (AU)
    T_star = 5778  # Surface Temperature of star (K)
    e = inputE  # Eccentricity of planet
    Period_Fractions = 10000  # number of fractions of period

    # Init
    period = math.pow(d_planet, 1.5)  # Period of planet's orbit (years)
    Power_output = (4 * math.pi * R_star ** 2 * sigma * T_star ** 4) / (
            4 * math.pi * d_planet ** 2)  # Power output of star (Watts)

    t = [0]
    T = [0]
    heat_in = []

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

    for i in range(steps):
        t.append(t[-1] + (period / Period_Fractions))
        heat_out = epsilon * sigma * pow(T[-1], 4)

        heat_content += (heat_in[i % Period_Fractions] - heat_out) * period / Period_Fractions * SiY
        T.append(heat_content / heat_capacity)  # (K)
        # print(t[-1], T[-1])  # For Debugging

    return t, T
