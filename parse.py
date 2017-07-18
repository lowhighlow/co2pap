#imports
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

#functions
def toStr(n):

    if (n < 10):
        return '00' + str(n)
    elif (n < 100):
        return '0' + str(n)
    else:
        return str(n)

def get(n):
    return df[n - 4]

def dropNan(c):
    c = c['Time']
    k = 0
    while True:
        try:
            if math.isnan(c[k]):
                c.drop(k)
                c.drop(k)
            else:
                k += 1
        except KeyError:
            break
    
        

#main code
csv = pd.read_csv('/home/gustav/PowerConsumptionData/n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
df = [pd.DataFrame(csv)]
l = 5
while True:
    try:
        currentDF = pd.DataFrame(pd.read_csv('/home/gustav/PowerConsumptionData/n' + toStr(l), sep='\s*,\s*', header=0, encoding='ascii', engine='python'))
        dropNan(currentDF)
        df.append(currentDF)
        print('Loaded n' + toStr(l))
        l += 1
    except FileNotFoundError:
        break

print(get(4)[1492020000])


