from tools import Table
from math import sqrt

coefficients = Table(["SET","Time Interval Range (s)","a","b","c"])

coefficients.set_content(
    [
        [1,"1<T<=5",0.2253,-20.7652,570.5679],
        [2,"5<T<=10",-0.1284,46.9861,-2651.88889],
        [3,"10<T<=100",0.1972,-19.3450,692.1201],
        [4,"100<T<=1000",0.2617,-56.2407,5957.7934],
        [5,"T>1000",0.3177,-136.2571,34522.4680]
    ]
)

def R_from_T(T):
    if 1 < T <= 5:
        mySet = coefficients.content[0]
    elif 5 < T <= 10:
        mySet = coefficients.content[1]
    elif 10 < T <= 100:
        mySet = coefficients.content[2]
    elif 100 < T <= 1000:
        mySet = coefficients.content[3]
    elif T > 1000:
        mySet = coefficients.content[4]
    
    a = mySet[2]
    b = mySet[3]
    c = mySet[4]
    
    #print("T= ",T)
    #print("using set for: ",mySet[1])

    R = 100 * ( (-b+sqrt(b*b-4*a*(c-100*T))) / (2*a) )

    return R


def T_from_R(R):
    if (R_from_T(2) < R <= R_from_T(5)):
        mySet = coefficients.content[0]
        #print("found",R_from_T(2),R_from_T(5))
        
    if (R_from_T(5) < R <= R_from_T(10)):
        mySet = coefficients.content[1]
        #print("found",R_from_T(5),R_from_T(10))
        
    if (R_from_T(10) < R <= R_from_T(100)):
        mySet = coefficients.content[2]
        #print("found",R_from_T(10),R_from_T(100))
        
    if (R_from_T(100) < R <= R_from_T(1000)):
        mySet = coefficients.content[3]
        #print("found",R_from_T(100),R_from_T(1000))
        
    if (R_from_T(1000) < R):
        mySet = coefficients.content[4]
        #print("found",R_from_T(1000))

            
    a = mySet[2]
    b = mySet[3]
    c = mySet[4]
    
    print("set: ",mySet[1])
    T = (10.0**-6) * a * R**2 + (10.0**-4) * b * R + (10.0**-2) * c
    
    return T

    


print("--- For Range: 1<T<=5 ---")
print("R_min:",R_from_T(2))
print("R_max:",R_from_T(5))

print("--- For Range: 5<T<=10 ---")
print("R_min:",R_from_T(5))
print("R_max:",R_from_T(10))

print("--- For Range: 10<T<=100 ---")
print("R_min:",R_from_T(10))
print("R_max:",R_from_T(100))

print("--- For Range: 100<T<=1000 ---")
print("R_min:",R_from_T(100))
print("R_max:",R_from_T(1000))

print("--- For Range: T>1000 ---")
print("R_min:",R_from_T(1000))


print("-------------------------------")

#T = 300

R = R_from_T(15*60)
#R = 9800

print("R in Ohms:",R)
print("R in kOhms:",round(R/1000,2))

Tnew = T_from_R(67*1000)

print("T in seconds:",Tnew)
print("T in minutes:",round(Tnew/60,2))

