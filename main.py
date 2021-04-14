from Utility import savePlot
from models.insolation_multiple import *
from models.latitude_stepping_GHE import *
from models.oneD import *
from models.oneD_GHE import *
from models.zeroD import *
from models.zeroD_GHE import *
from models.zeroD_e import *
from models.zeroD_e_bar import *
from models.zeroD_e_mmm import *

print("Which model would you like to see?")
print("0 - OD EBM")
print("1 - OD EBM w/ eccentricity variation")
print("2 - OD EBM w/ eccentricity variation - Bar")
print("3 - OD EBM w/ eccentricity variation - Min/Max/Mean")
print("4 - OD EBM w/ Greenhouse effect")
print("5 - 1D EBM")
print("6 - 1D EBM w/ Greenhouse effect")
print("7 - Solar insolation on Eccentric orbit")
print("8 - Solar insolation on different eccentric orbits")
print("9 - Latitude stepping 1D EBM w/ Greenhouse Effect")
selection = int(input())

if selection == 0:
    print("0D EBM")

    fig = zeroD_EBM('0D EBM')
    plt.show()
    savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '0D EBM')

elif selection == 1:
    print("0D EBM w/ eccentricity variation")

    fig = zeroD_e('0D EBM with eccentricity variation')
    plt.show()
    savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '0D EBM with eccentricity variation')

elif selection == 2:
    print("OD EBM w/ eccentricity variation - Bar")

    fig = zeroD_e_bar('OD EBM w/ eccentricity variation - Bar')
    plt.show()
    savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '0D EBM with eccentricity variation - Bar', 3200)

elif selection == 3:
    print("OD EBM w/ eccentricity variation - Min/Max/Mean")

    fig = zeroD_e_mmm("OD EBM with eccentricity variation - Min/Max/Mean")
    plt.show()
    savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', 'OD EBM with eccentricity variation - Min/Max/Mean', 3200)

elif selection == 4:
    print("OD EBM w/ Greenhouse effect")

    fig = zeroD_GHE('0D EBM with Greenhouse Effect')
    plt.show()
    savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '0D EBM with Greenhouse Effect')

    # t, T = zeroD_GHE()
    # fig, plt = plotGraph(t, T, '0D EBM with Greenhouse Effect', 'time (years)', 'Surface temperature (K)', 'true')
    # plt.annotate(str(round(T[-1], 3)), (t[-1], T[-1]), xycoords='data', xytext=(t[-1] - 125, T[-1] - 20))
    # # savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '0D EBM with Greenhouse Effect')
    #
    # plt.show()

elif selection == 5:
    print("1D EBM")
    fig, plt = oneD()  # TODO
    # savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '1D EBM without Greenhouse Effect')
    plt.show()

elif selection == 6:
    print("1D EBM w/ Greenhouse effect")
    fig, plt = oneD_GHE()  # TODO
    # savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', '1D EBM with Greenhouse Effect')
    plt.show()

elif selection == 7:
    print("Solar insolation on Eccentric orbit")

    fig = insolation_single()  # TODO
    # fig, plt = plotGraph(t, L, 'Light insolation on an eccentric orbit (e = 0.01671)', 'time (days)',
    #                      'Light Insolation (W/m^2)', 'false')
    #
    # # savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', 'Light Insolation on an Eccentric Orbit')
    # plt.show()

elif selection == 8:
    print("Solar insolation on different eccentric orbits")

    fig, plt = insolation_multiple()  # TODO
    # savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', 'Solar insolation on different eccentric orbits')
    plt.show()

elif selection == 9:
    print("Latitude stepping 1D EBM w/ Greenhouse Effect")

    t, T = latitude_stepping_GHE()  # TODO
    fig, plt = plotGraph(t, T, 'Latitude Stepping 1D EBM with GHE', 'Latitude (°)', 'Stable Surface Temperature (K)',
                         'true')
    # savePlot(fig, 'C:\\Users\\Michal\\Desktop\\Remote Lessons\\CREST\\dump\\', 'Latitude Stepping 1D EBM with GHE')

    plt.show()
