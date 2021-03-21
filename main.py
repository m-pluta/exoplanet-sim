from Utility import *
from models.zeroD import *

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
    t, T = zeroD_EBM()
    plotGraph(t, T, '0D EBM without Greenhouse effect', 'time (years)', 'Surface temperature (K)', 'true')

elif selection == 1:
    print("OD EBM w/ eccentricity variation")
elif selection == 2:
    print("OD EBM w/ eccentricity variation")
elif selection == 3:
    print("OD EBM w/ eccentricity variation")
elif selection == 4:
    print("OD EBM w/ eccentricity variation")
elif selection == 5:
    print("OD EBM w/ eccentricity variation")
elif selection == 6:
    print("OD EBM w/ eccentricity variation")
elif selection == 7:
    print("OD EBM w/ eccentricity variation")
elif selection == 8:
    print("OD EBM w/ eccentricity variation")
elif selection == 9:
    print("OD EBM w/ eccentricity variation")
