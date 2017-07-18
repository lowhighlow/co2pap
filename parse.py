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

def get(dataframes, n):
    return dataframes[n - 4]

def dropNan(raw):
    
    edit = raw;
    bitmask = np.isnan(raw.ttl_pwr)
    occurences = []
    occurences = np.argwhere(bitmask == True)
    k = 0
    
    if len(occurences) != 0:
        while k < len(occurences):
            
            bitmask[occurences[k] + 1] = True
            
            k += 1
    

    
    edit = edit[np.invert(bitmask)]
    return edit
    
        

#main code
if __name__ == '__main__':
    csv = pd.read_csv('/home/gustav/PowerConsumptionData/n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    dataframes = [pd.DataFrame(csv)]
    print('Loaded n004')
    dataframes[0] = dropNan(dataframes[0])
    l = 5
    print(len(get(dataframes, 4)))
    print(get(dataframes, 4).ttl_pwr.values[724])

    


