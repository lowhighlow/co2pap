import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

<<<<<<< master
csv = pd.read_csv('/home/gustav/PowerConsumptionData/n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
df = pd.DataFrame(csv)
plt.plot(df['Time'])
plt.show()
=======
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

#main code
csv = pd.read_csv('/home/gustav/PowerConsumptionData/n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
df = [pd.DataFrame(csv)]
l = 5
while True:
    try:
        currentDF = pd.DataFrame(pd.read_csv('/home/gustav/PowerConsumptionData/n' + toStr(l), sep='\s*,\s*', header=0, encoding='ascii', engine='python'))
        df.append(currentDF)
        print('Loaded n' + toStr(l))
        l += 1
    except FileNotFoundError:
        break

>>>>>>> local

