import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


def ToTFunc(N, Ape, C, k):
    
    return np.sqrt(Ape*N/C) + k


if __name__ == "__main__":
    xData = [1,2,3,4,5,6,7,8,9]
    yData = [24,36,45,52,58,64,70,74,78]
    

    print(xData)

    pOpt, pCov = curve_fit(ToTFunc, xData, yData)

    xVals = np.linspace(1, 600, 300)
    
    plt.plot(xData, yData, 'x')
    plt.plot(xVals, ToTFunc(xVals, *pOpt))
    plt.xlabel("PE")
    plt.ylabel("ToT (ns)")
    plt.show()
