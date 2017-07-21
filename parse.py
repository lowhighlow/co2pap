#imports
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import time as time
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches

import fileinput

#Vals
interval = 60


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
        while k < len(occurences) - 1:
            
            bitmask[occurences[k] + 1] = True
            
            k += 1
    

    
    edit = edit[np.invert(bitmask)]
    return edit




def findTime(df, time1, time2):
    
    timetable = df[(df['Time'] >= time1) & (df['Time'] <= time2)]

    print (df['Time'])
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

def totalConsumption(nodeframe):
    
    power = calculateTotalPowerConsumption(dataframes, nodeframe).ttl_pwr / 1000
    
    print('It were:')
    print(str(int(power)) + ' kWh energy used.')
    print(str(int(powerToCO2(power))) + ' kG CO² emitted.')
    print(str(int(powerToMoney(power))) + ' € spent.')

def calculateInterval(dataframe):
    return dataframe.Time.iloc[1] - dataframe.Time.iloc[0]


def saveToChart(dataframes, nodeframe, power, name, t1, t2):
    with PdfPages('Chart.pdf') as pdf:


        #n = 1
        #colors = [(0, 0, 255)]
        #while n < len(nodeframe.node):
            #colors[n] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        n = 0
        plt.axis([t1,t2, 0, 300])
        plt.title('Total Consumption')
        while n < len(nodeframe.node):
        
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].ttl_pwr.values)
            n+=1
        plt.ylabel('Wh')
        plt.xlabel('Seconds since Epoch')
        pdf.savefig()
        pdf.savefig()
        plt.close()

        n = 0
        plt.axis([t1,t2, 0, 250])
        plt.title('CPU Consumption')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].cpu_pwr.values)
            n+=1
        plt.ylabel('Wh')
        plt.xlabel('Seconds since Epoch')
        pdf.savefig()
        plt.close()

        plt.axis([t1,t2, 0, 100])
        plt.title('Memory Consumption')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].mem_pwr.values)
            n+=1
        plt.ylabel('Wh')
        plt.xlabel('Seconds since Epoch')
        pdf.savefig()
        plt.close()

        plt.axis([t1,t2, 0, 16])
        plt.title('CPU Load')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].cpu_load.values)
            n+=1
        plt.ylabel('Load')
        plt.xlabel('Seconds since Epoch')
        pdf.savefig()
        plt.close()

        plt.axis([t1,t2, 0, 10])
        plt.title('Memory Load')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].mem_load.values)
            n+=1
        plt.ylabel('Laoad')
        plt.xlabel('Seconds since Epoch')
        pdf.savefig()
        plt.close()
            

    
    

#main code
if __name__ == '__main__':
    csv = pd.read_csv('n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    
    
    dataframes = [pd.DataFrame(csv)]
    print('Loading started')
    interval = calculateInterval(dataframes[0])
    
    
    dataframes[0] = dropNan(dataframes[0])
    l = 5
    while True:
        try:
                    
            currentDF = pd.DataFrame(pd.read_csv('n' + toStr(l), sep='\s*,\s*', header=0, encoding='ascii', engine='python'))
            currentDF = dropNan(currentDF)
            dataframes.append(currentDF)
            l += 1
        except FileNotFoundError:
            if l > 128:
                break
            l += 1
    print('Loading finished')

    #Testing Area
    csv = pd.read_csv('nodeframe', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    nodeframe = pd.DataFrame(csv)
    
    power = calculateTotalPowerConsumption(dataframes, nodeframe).ttl_pwr / 1000
    saveToChart(dataframes, nodeframe, power, "calc2", 1500441000, 1500528600)
    totalConsumption(nodeframe)
    

