import sympy
from table import Table

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

