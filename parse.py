#imports
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import time as time
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
import os

#Vals

#interval is the diffrence between two sequential timestamps
interval = 60
#times for passing to extrct_....
start = str(-3600*48)
end = '-100'


#functions

#converts n to a string in the format 004 / 044 / 444
def toStr(n):

    if (n < 10):
        return '00' + str(n)
    elif (n < 100):
        return '0' + str(n)
    else:
        return str(n)


#returns the dataframe out of an list corresponding to the node n
def get(dataframes, n):
    return dataframes[n - 4]

#drops nans for a passed dataframe
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



#returns a part from a dataframe wich timestamp is between time1 and time2
def findTime(df, time1, time2):
    
    timetable = df[(df['Time'] >= time1) & (df['Time'] <= time2)]

    if timetable.tail(1).Time.iloc[0] < time2:
        timetable = timetable.append(df[(df['Time'] >= time2) & (df['Time'] <= time2 + interval)])
    
    if timetable.Time.iloc[0] > time1:
        timetable2 = df[(df['Time'] <= time1) & (df['Time'] >= time1 + interval)]
        timetable = timetable2.append(timetable)
        
    return timetable
    


#calculates the Mem consumption of a Dataframe (node) between start and end (only usable with .mem_pwr)
def calculateMEMConsumption(node, start, end):
    timetable = findTime(node, start, end)
    power = 0
   
    if timetable.Time.iloc[0] > start:
        
        power += (timetable.Time.iloc[0] - start) * timetable.mem_pwr.iloc[0]
    else:
        power += interval * timetable.mem_pwr.iloc[0]

    n = 1
    while n < timetable.Time.size -1:
        power += interval * timetable.mem_pwr.iloc[n]
        n += 1
    
    if timetable.tail(1).Time.iloc[0] > end:
        power += (timetable.tail(1).Time.iloc[0] - end) * timetable.tail(1).iloc[0]
    else:
        power += interval * timetable.tail(1).iloc[0]
        
    
    return power / 3600

#calculates the CPU consumption of a Dataframe (node) between start and end (only usable with .mem_pwr)
def calculateCPUConsumption(node, start, end):
    timetable = findTime(node, start, end)
    power = 0
   
    if timetable.Time.iloc[0] > start:
        
        power += (timetable.Time.iloc[0] - start) * timetable.cpu_pwr.iloc[0]
    else:
        power += interval * timetable.cpu_pwr.iloc[0]

    n = 1
    while n < timetable.Time.size -1:
        power += interval * timetable.cpu_pwr.iloc[n]
        n += 1
    
    if timetable.tail(1).Time.iloc[0] > end:
        power += (timetable.tail(1).Time.iloc[0] - end) * timetable.tail(1).iloc[0]
    else:
        power += interval * timetable.tail(1).iloc[0]
        
    
    return power / 3600
#calculates the consumption of a Dataframe (node) between start and end (only usable with .ttl_pwr)
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

#calculates the consumption of Multiple nodes passed as a Dataframe in the nodeframe format 
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

#Converts and prints power etc for multiple nodes (nodeframe format)
def totalConsumption(nodeframe):
    
    power = calculateTotalPowerConsumption(dataframes, nodeframe).ttl_pwr / 1000
    
    print('It were:')
    print(str(int(power)) + ' kWh energy used.')
    print(str(int(powerToCO2(power))) + ' kG CO² emitted.')
    print(str(int(powerToMoney(power))) + ' € spent.')

#calculates the Interval any dataframe is passable
def calculateInterval(dataframe):
    return dataframe.Time.iloc[1] - dataframe.Time.iloc[0]

#saves to chart
def saveToChart(dataframes, nodeframe, name, t1, t2):
    with PdfPages('Chart.pdf') as pdf:


        
        
        n = 0
        plt.axis([t1,t2, 0, 300])
        plt.title('Total Consumption')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].ttl_pwr.values, label='n' + toStr(n))
            n+=1
        plt.ylabel('Wh')
        plt.xlabel('Seconds since Epoch')
        plt.legend(loc='best')

        pdf.savefig()
        pdf.savefig()
        plt.close()

        n = 0
        plt.axis([t1,t2, 0, 250])
        plt.title('CPU Consumption')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].cpu_pwr.values, label='n' + toStr(n))
            n+=1
        plt.ylabel('Wh')
        plt.xlabel('Seconds since Epoch')
        plt.legend(loc='best')
        pdf.savefig()
        plt.close()

        n = 0
        plt.axis([t1,t2, 0, 100])
        plt.title('Memory Consumption')
        plt.subplots()
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].mem_pwr.values, label='n' + toStr(n))
            n+=1
        plt.ylabel('Wh')
        plt.xlabel('Seconds since Epoch')
        plt.legend(loc='best')
        pdf.savefig()
        plt.close()

        n = 0
        plt.axis([t1,t2, 0, 40])
        plt.title('CPU Load')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].cpu_load.values, label='n' + toStr(n))
            n+=1
        plt.ylabel('Load')
        plt.xlabel('Seconds since Epoch')
        plt.legend(loc='best')
        pdf.savefig()
        plt.close()
        
        n = 0
        plt.axis([t1,t2, 0, 40000])
        plt.title('Memory Load')
        while n < len(nodeframe.node):
            
            plt.plot(dataframes[nodeframe.node.iloc[n]].Time.values, dataframes[nodeframe.node.iloc[n]].mem_load.values, label='n' + toStr(n))
            n+=1
        plt.ylabel('Laoad')
        plt.xlabel('Seconds since Epoch')
        plt.legend(loc='best')
        pdf.savefig()
        plt.close()
            


        #piechart
        labels = ['Cpu consumption', 'Memory\nconsumption', 'Other factors']
        node = get(dataframes, nodeframe.node.iloc[0])
        div = calculatePowerConsumption(node, t1, t2).ttl_pwr - calculateCPUConsumption(node, t1, t2).cpu_pwr - calculateMEMConsumption(node, t1, t2).mem_pwr 
        sizes = [calculateCPUConsumption(node, t1, t2).cpu_pwr / calculatePowerConsumption(node, t1, t2).ttl_pwr, calculateMEMConsumption(node, t1, t2).mem_pwr / calculatePowerConsumption(node, t1, t2).ttl_pwr, div / calculatePowerConsumption(node, t1, t2).ttl_pwr]
        plt.pie(sizes, labels=labels, shadow=True, startangle=90)
        plt.title('Percentual Consumtion for n' + toStr(nodeframe.node.iloc[0]))
        pdf.savefig()
        plt.close()

        
    

#main code
if __name__ == '__main__':



    #saves start and end to file for interaction with extr_.......
    f = open('interactionfile', 'w')
    f.write(str(start) + '\n' + str(end))
    f.close()
    time.sleep(5)
    os.system('python2 extrct_mntrng_infrmtn.py')
    time.sleep(20)


    #loads dataframes
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
    saveToChart(dataframes, nodeframe, "calc2", 1500441000, 1500528600)
    totalConsumption(nodeframe)
    

