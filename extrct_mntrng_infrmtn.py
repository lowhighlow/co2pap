
from datetime import datetime
import time
from subprocess import Popen,PIPE,call
import sys,os,glob,getopt,pickle,re,commands
import string
import csv

f=open('interactionfile', 'r')

strt=f.readline().replace('\n', '')
end=f.readline()
f.close()

list=[]

for i in range(4,129):
	if i%2 != 0:
		dict={"cpu_load":"CPU_load_load15","mem_load":"Memory_used_memused","cpu_pwr":"IPMI_Sensor_CPU_Avg_Power_CPU_Avg_Power","mem_pwr":"IPMI_Sensor_MEM_Avg_Power_MEM_Avg_Power","ttl_pwr":"IPMI_Sensor_Domain_A_AvgPwr_Domain_A_AvgPwr"}
	else:
		dict={"cpu_load":"CPU_load_load15","mem_load":"Memory_used_memused","cpu_pwr":"IPMI_Sensor_CPU_Avg_Power_CPU_Avg_Power","mem_pwr":"IPMI_Sensor_MEM_Avg_Power_MEM_Avg_Power","ttl_pwr":"IPMI_Sensor_Domain_B_AvgPwr_Domain_B_AvgPwr"}

	nmbr=str(i).zfill(3)

	for key in dict:
		out, err = Popen("rrdtool fetch /tmp/check_mk/pnp4nagios/perfdata/n%s/%s.rrd AVERAGE -s %s -e %s" % (nmbr,dict[key],strt,end), shell=True, stdout=PIPE).communicate()

		if len(list) == 0:
			for ln in out.split("\n"):
				if ":" in ln:
					dct={}
					dct['Time']=ln.split(":")[0]
					dct[key]=ln.split(":")[1]
					list.append(dct)
		else:
			i=0
			for ln in out.split("\n"):
				if ":" in ln:
					if len(list) > i :
						if list[i]['Time'] == ln.split(":")[0]:
							list[i][key]=ln.split(":")[1]
						i+=1
					else:
						dct={}
						dct['Time']=ln.split(":")[0]
						dct[key]=ln.split(":")[1]
						list.append(dct)

	with open("n%s" % nmbr, 'w') as f:
		strng=""	
		for k,v in list[0].items():
			if k == "Time":
				strng=" %s," % k + strng
			else:
				strng=strng+" %s," % k

		strng1=strng[:-1] + "\n"

		f.write(strng1)

		i=0
		lngth=len(list)

		while i < lngth:
			strng=""	
			for k,v in list[i].items():
				if k == "Time":
					strng=" %s," % v + strng
				else:
					strng=strng+"%s," % v

			strng1=strng[:-1] + "\n"

			f.write(strng1) 
			i+=1

