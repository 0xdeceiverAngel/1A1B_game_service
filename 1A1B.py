import requests
import os
import sys
import urllib.request
import time
import random
import socket

ans=""
while 1:
    if (len(ans) == 4):
        break
    inp = random.choice('0123456789')
    if inp not in ans:
        ans+=inp
print(ans)

while 1:
    sin=input('>')
    if (sin == ans):
        print('win')
        break
    A = 0
    B = 0
    for i in range(4):
        if (ans[i] == sin[i]):
            A = A + 1
        if (sin[i] in ans):
            B = B + 1
    B = B - A
    print(A,B)    


            
    
