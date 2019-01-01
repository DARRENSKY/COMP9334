
def p0(opreators,slots,r):
    k=opreators+slots
    r=r
    num0=1
    num1 = 1 * (r**1)
    num2 = (1 / 2) * (r**2)
    num3 = (1 / 6) * (r**3)
    num4=(1/24)*(r**4)
    num4beforesum=num0+num1+num2+num3+num4
    num4aftersum=0
    if k==0:
        return num0
    if k==1:
        return num1
    if k==2:
        return (num1+num2)
    if k==3:
        return (num1+num2+num3)
    if k==4:
        return (num1+num2+num3+num4)
    if k>4:
        for i in range(5,k+1):
            num4aftersum+=(1/24)*(1/4)**(i-4)*(r**i)
    num=num4beforesum+num4aftersum
    return 1/num
def pk(opreators,slots,k,r):
    p_0=p0(opreators,slots,r)
    p_1=p_0*1*(r**1)
    p_2=p_0*(1/2) * (r**2)
    p_3=p_0*(1/6) * (r**3)
    p_4=p_0*(1/24)*(r**4)
    if k==0:
        return p_0
    if k==1:
        return p_1
    if k==2:
        return p_2
    if k==3:
        return p_3
    if k==4:
        return p_4
    if k>4:
        p_k=p_0*((1/4)**(k-4))*(1/24)*(r**k)
        return p_k

opreators=4
slots=2
a=15
b=3
r=5
print("Question 2(e) results:\n")
print("Before adding waiting slots ")
p_k=pk(opreators,slots,opreators+slots,r)
p_0=p0(opreators,slots,r)
print('The value of P(0) is:',p_0)
print("The blocking probability is: ",p_k)
print()
print("After adding 5 waiting slots ")
newslots=slots+5
p_k=pk(opreators,newslots,opreators+newslots,r)
p_0=p0(opreators,newslots,r)
print('The value of P(0) is:',p_0)
print("The blocking probability is: ",p_k)
print()
print("After adding 10 waiting slots ")
newslots=slots+10
p_k=pk(opreators,newslots,opreators+newslots,r)
p_0=p0(opreators,newslots,r)
print('The value of P(0) is:',p_0)
print("The blocking probability is: ",p_k)
print()
print("After adding 15 waiting slots ")
newslots=slots+15
p_k=pk(opreators,newslots,opreators+newslots,r)
p_0=p0(opreators,newslots,r)
print('The value of P(0) is:',p_0)
print("The blocking probability is: ",p_k)
print()
print("After adding 20 waiting slots ")
newslots=slots+20
p_k=pk(opreators,newslots,opreators+newslots,r)
p_0=p0(opreators,newslots,r)
print('The value of P(0) is:',p_0)
print("The blocking probability is: ",p_k)