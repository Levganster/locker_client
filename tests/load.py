import os
import time

a ="██"
b ="▒"
c = 10
for i in range(c+1):
    os.system("cls")
    print(i*a,(c-i)*2*b)
    time.sleep(0.5)