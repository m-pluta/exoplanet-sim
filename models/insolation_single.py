import math

from Utility import distance_of_planet_to_star


def insolation_single(inputE):
    #  Sources: Kepler's First Law: https://www.vanderbilt.edu/AnS/physics/astrocourses/ast201/keplerslaws_1.html
    #                               http://astronomy.nmsu.edu/nicole/teaching/ASTR505/lectures/lecture08/slide13.html#:~:text=The%20squares%20of%20the%20sidereal,square%20of%20its%20sidereal%20period.

    R_star = 0.00465047  # Radius of star (AU)
    R_planet = 1  # Distance of planet from body it is orbiting  (AU)
    T_star = 5778  # (K)
    e = 0.01671  # Eccentricity of planet
    sigma = 5.67E-8  # Boltzmann constant
    timeStep = 1E-3  # fraction of period acts as timeStep

    # Init
    period = math.pow(R_planet, 1.5) * 365.25
    Power_output = (4 * math.pi * R_star ** 2 * sigma * T_star ** 4) / (4 * math.pi * R_planet ** 2)

    e = inputE

    t = []
    L = []

    # Generating Data
    for i in range(int(1 / timeStep)):
        t.append((i * timeStep) * period)
        theta = (i * timeStep) * 2 * math.pi  # Calculating angle in orbit
        r = distance_of_planet_to_star(theta, R_planet, e)  # Applying Kepler's First Law to find r
        newL = Power_output / (
                r / R_planet) ** 2  # Calculating insolation based on position in orbit relative to the starting point
        L.append(newL)

    return t, L
