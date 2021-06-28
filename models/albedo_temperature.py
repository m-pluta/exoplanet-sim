from Utility import *


def albedo_temperature(plotTitle):
    T = generateList(250, 300, 0.1)
    A_linear = []
    A_quadratic = []
    for Temp in T:
        A_linear.append(smoothAlbedo_linear(Temp))
        A_quadratic.append(smoothAlbedo_quadratic(Temp))

    # Plotting data
    fig = plt.figure(plotTitle)
    plt.plot(T, A_linear, c='c', linewidth=1.75, linestyle='dashed', label='Linear')
    plt.plot(T, A_quadratic, c='r', linewidth=1.75, label='Quadratic')

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'Temperature (K)', 'Albedo')
    fig = addLegend(fig, 'upper right', 'Smoothing Types: ')

    return fig


def smoothAlbedo_linear(currentTemp, iceAlbedoThreshold=260, MinAlbedoTemperature=293, minAlbedo=0.289, maxAlbedo=0.7):
    if currentTemp < iceAlbedoThreshold:
        return maxAlbedo
    elif iceAlbedoThreshold <= currentTemp <= MinAlbedoTemperature:
        # ensures albedo transitions smoothly between 0.7 and 0.3 depending on temperature - this is basically linear interpolation
        return maxAlbedo - (maxAlbedo - minAlbedo) * (currentTemp - iceAlbedoThreshold) / (MinAlbedoTemperature - iceAlbedoThreshold)
    else:
        return minAlbedo


def smoothAlbedo_quadratic(Temp, T_i=260, T_o=293, alpha_o=0.289, alpha_i=0.7):
    if Temp <= T_i:
        return alpha_i
    elif T_i < Temp < T_o:
        return alpha_o + (alpha_i - alpha_o) * ((Temp - T_o) ** 2) / ((T_i - T_o) ** 2)
    else:
        return alpha_o
