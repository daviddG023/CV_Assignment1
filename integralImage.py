import numpy as np
def printArray(array):  
    for i in range(len(array)):
        for j in range(len(array[i])):
            print(array[i][j], end=" ")
        print()

def RowIntegral(array):
    newArray = np.zeros((len(array), len(array[0])), dtype=np.int64)
    for i in range(len(array)):
        for j in range(len(array[i])):
            if(j == 0):
                newArray[i][j] = array[i][j]
            else:
                newArray[i][j] = newArray[i][j-1] + array[i][j]
    return newArray
def ColumnIntegral(array):
    newArray = np.zeros((len(array), len(array[0])), dtype=np.int64)
    for i in range(len(array)):
        for j in range(len(array[i])):
            if(i == 0):
                newArray[i][j] = array[i][j]
            else:
                newArray[i][j] = newArray[i-1][j] + array[i][j]
    return newArray

def doubleIntegral(array):
    return ColumnIntegral(RowIntegral(array))

def LocalSum(array, x1, y1, x2, y2):
    s = array[x2, y2]
    if x1 > 0: s -= array[x1-1, y2]
    if y1 > 0: s -= array[x2, y1-1]
    if x1 > 0 and y1 > 0: s += array[x1-1, y1-1]
    return s