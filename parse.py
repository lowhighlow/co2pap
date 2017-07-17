import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv = pd.read_csv('/home/gustav/PowerConsumptionData/n004', sep='\s*,\s*', header=0, encoding='ascii', engine='python')
df = pd.DataFrame(csv)
plt.plot(df['Time'])
plt.show()

