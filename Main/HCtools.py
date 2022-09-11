# this module contains function necessary in other modules

import numpy as np
import math as mt


# interpolate data "D" based on its timestamps "Pd" and the required interpolated timestamps "P"

def dateintpol(D, Pd, P):
    # D = full date array
    # Pd = non interpolated data date array
    # P = data to be interpolated
    Dsize = len(D)
    FullP = np.zeros(Dsize)
    FullP[0] = P[0]
    i = 0
    j = 0
    while j < Dsize and i < len(P):
        Diff = (Pd[i] - D[j]).days
        if Diff == 0:
            FullP[j] = P[i]
            i += 1
            j += 1
        else:
            delta = (P[i] - P[i - 1]) / (Diff + 1)
            n = j + Diff
            FullP[j:n] = delta * np.arange(1, (Diff + 1)) + P[i - 1]
            j += Diff
    return FullP


# interpolate data where zeros are found

def zerintpol(X):
    len_x = len(X)
    P = np.zeros(len(X))
    i = 0
    j = 0
    while i < len_x:
        if X[i] != 0:
            if i == j:
                P[i] = X[i]
                i += 1
                j += 1
            else:
                P[j:i] = ((X[i] - X[j - 1]) / (i - j + 1)) * np.arange(1, i - j + 1) + X[j - 1]
                P[i] = X[i]
                i += 1
                j = i
        elif X[i] == 0 and i != (len_x - 1):
            i += 1
        elif X[i] == 0 and i == (len_x - 1):
            P[j:i+1] = X[j - 1]
            i += 1
    return P


# truncation functions

def truncd(x):
    a = mt.floor(x * 10) / 10
    return a

def truncc(x):
    a = mt.floor(x * 100) / 100
    return a

def truncm(x):
    a = mt.floor(x * 1000) / 1000
    return a

def truncdm(x):
    a = mt.floor(x * 10000) / 10000
    return a
