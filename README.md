This project is intended to calculate the power consumption for individual projects at the cluster computer.
In order for it to work it needs acces to csv-files named n004 to n... at the path written in the code. And a csv-file named
nodeframe in the same folder as the script. 

The format for the n... file needs to be like this:

 Time, ttl_pwr, cpu_pwr, mem_pwr, cpu_load, mem_load
 
 1483228800, 1.7306365741e+02, 1.1758435185e+02, 3.7052962963e+01, 8.8779824074e+00, 2.9319143241e+04
 1483250400, 1.7047314815e+02, 1.1539787037e+02, 3.6647314815e+01, 8.4709282407e+00, 2.9207021620e+04
 
And for the nodeframe:

 node, time1, time2
 4, 1483228800, 1498867200
 
All Timerelated rows need to be in the Unix-Timestamp in order for it to work. The interval variable needs to be changed to the
interval between two measurments in seconds.
