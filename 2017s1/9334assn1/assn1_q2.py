# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 17:59:59 2017

@author: DELL
"""


ro=10/3
m = 0
p_m=1
p_0 = 1
queue=0

while p_m > 0.24258/2:
    m+=1
    new=(ro/4)**(m+1)*(ro**3)/6
    queue+=new
    x=1+ro+0.5*ro**2+(ro**3)/6+(ro**4)/24+queue
    p_0=1/x
    p_m=(ro/4)**(m+1)*(ro)**3*p_0 /6
    
# Posibilities from P0 to P7   
l=[p_0,ro*p_0 , ro**2/2*p_0,ro**3/6*p_0 , ro**4/24*p_0 , (ro)**3*p_0*(ro/4)**2/6,
      (ro)**3*p_0*(ro/4)**3/6 , (ro)**3*p_0*(ro/4)**4/6]
    


print("Pm=",p_m)
print("number of stacks=",m)
avg=0
for i in range(len(l)):
    avg+=i*l[i]
    print("P{:}=".format(i),l[i])
print("Avg_jobs=",avg)
print("Waiting time={:} hours".format(avg/20-1/6))  #Waiting time=response time-service time
