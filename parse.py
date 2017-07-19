#imports
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

#Vals
interval = 21600

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




def findTime(df, time1, time2):
    
    timetable = df[(df['Time'] >= time1) & (df['Time'] <= time2)]

    
    if timetable.tail(1).Time.iloc[0] < time2:
        timetable = timetable.append(df[(df['Time'] >= time2) & (df['Time'] <= time2 + interval)])
    
    if timetable.Time.iloc[0] > time1:
        timetable2 = df[(df['Time'] <= time1) & (df['Time'] >= time1 + interval)]
        timetable = timetable2.append(timetable)
        
    return timetable
    

def calculatePowerConsumption(node, start, end):
    timetable = findTime(node, start, end)
    power = 0
   
    if timetable.Time.iloc[0] > start:
        
        power += (timetable.Time.iloc[0] - start) * timetable.ttl_pwr.iloc[0]
    else:
        power += interval * timetable.ttl_pwr.iloc[0]

    n = 1
    while n < timetable.Time.size -1:
        power += interval * timetable.ttl_pwr.iloc[n]
        n += 1
    
    if timetable.tail(1).Time.iloc[0] > end:
        power += (timetable.tail(1).Time.iloc[0] - end) * timetable.tail(1).iloc[0]
    else:
        power += interval * timetable.tail(1).iloc[0]
        
    
    return power / 3600

def calculateTotalPowerConsumption(dataframes, nodeframe):
    totalpower = 0
    n = 0
    while n < nodeframe.node.size:
        totalpower += calculatePowerConsumption(get(dataframes, nodeframe.node.iloc[n]), nodeframe.time1.iloc[n], nodeframe.time2.iloc[n])
        n += 1
    return totalpower

def powerToCO2(n):
    return n * 0.197

def powerToMoney(n):
    return n * 0.2

#main code
if __name__ == '__main__':
    csv = pd.read_csv('/home/gustav/PowerConsumptionData/n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    dataframes = [pd.DataFrame(csv)]
    print('Loading started')
    dataframes[0] = dropNan(dataframes[0])
    l = 5
    while True:
        try:
            currentDF = pd.DataFrame(pd.read_csv('/home/gustav/PowerConsumptionData/n' + toStr(l), sep='\s*,\s*', header=0, encoding='ascii', engine='python'))
            currentDF = dropNan(currentDF)
            dataframes.append(currentDF)
            
            l += 1
        except FileNotFoundError:
            break
    print('Loading finished')

    #Testing Area
    csv = pd.read_csv('nodeframe', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    nodeframe = pd.DataFrame(csv)
    power = calculateTotalPowerConsumption(dataframes, nodeframe).ttl_pwr / 1000
    print('Es wurden ungefähr im letzten halben Jahr für node 4:')
    print(str(int(power)) + ' kWh Strom verbraucht')
    print(str(int(powerToCO2(power))) + ' kG CO² ausgestoßen')
    print(str(int(powerToMoney(power))) + ' € Ausgegeben')
