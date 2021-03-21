def zeroD_GHE():
    # Constants
    timeStep = 0.1  # years
    waterDepth = 4000  # metres
    L = 1361  # W/m^2
    albedo = 0.3
    epsilonS = 1.0
    epsilonA = 0.77
    sigma = 5.67E-8  # W/m^2/K^4
    heatCapacity = waterDepth * 4.2E6  # JK/m^2
    FluxIn = L * (1 - albedo) / 4  # W/m^2
    SiY = 31536000  # Seconds in year

    # Declaring variables and initialisation
    t = [0]
    T = [0]  # K
    heatContent = 0  # J/m^2
    FluxOut = 0  # W/m^2
    FluxNet = FluxIn - FluxOut

    years = 1500  # Arbitrary value
    for i in range(1, int(years / timeStep)):
        # tempA = ((epsilonS*sigma*T[-1]**4-(1-epsilonA)*epsilonS*sigma*T[-1]**4)/(2*sigma*epsilonA))**0.25
        tempA = (0.5 * epsilonS * (T[-1] ** 4)) ** 0.25  # Simplified equation
        heatContent += FluxNet * SiY * timeStep
        T.append(heatContent / heatCapacity)
        FluxOut = (1 - epsilonA) * (epsilonS * sigma * T[-1] ** 4) + (epsilonA * sigma * tempA ** 4)
        FluxNet = FluxIn - FluxOut

        t.append(t[-1] + timeStep)

    return t, T
