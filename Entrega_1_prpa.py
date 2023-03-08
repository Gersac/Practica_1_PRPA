#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:34:36 2023

@author: alumno

Entrega 1
Germán Sánchez Cuesta
"""


import time
import random
from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore


NProd=5
N=10



def producer (index,prob,storage,full,sem_prod):
    for i in range(N):
      d=random.randint(prob.value+1,prob.value+5)
      prob.value+=1
      print(f"producer {current_process().name} produce {d}\n")  
      if storage[index]==-2:
        storage[index]=d
        print(f"producer {current_process().name} almacena {d}\n")
      full.release()
      sem_prod.acquire()
    full.release()
    storage[index]=-1
    
    
    
def consumer(stor2,prob,full,sem):
    storage=[]
    for i in range(NProd):
        full[i].acquire()
    while todo1neg(stor2):
     print(f"El almacen es [{stor2[0]},{stor2[1]},{stor2[2]},{stor2[3]},{stor2[4]}]")
     minimo=10**8    
     for i in range(NProd):
        if stor2[i] > 0 and stor2[i]<minimo:
            minimo=stor2[i]
            pos=i
     storage.append(minimo)
     prob.value=minimo
     print (f"consumer consumiendo {minimo}\n")
     stor2[pos]=-2
     sem[pos].release()
     full[pos].acquire()
    print(f"El almacen final es {storage}")

def todo1neg(storage):
    val=False
    for a in range(NProd):
        if storage[a]!=-1:
            val=True
    return val        

def main():
    stor2=Array('i',NProd)
    for i in range(NProd):
        stor2[i]=-2   
    full=[]
    sem=[]
    for i in range(NProd):
        sem.append(Semaphore(0))
        full.append(Semaphore(0))
    index=Value('i',0)
    prob=Value('i',0)
    prd=[]
    index.value=0
    for j in range(NProd):
        prd.append(Process(target=producer, name = f'prod_{j}', args = (index.value,prob, stor2, full[index.value], sem[index.value])))
        index.value+=1
    
    q=Process(target=consumer,args=(stor2,prob,full,sem))
    for p in prd:
        p.start()  
    q.start()    
    for p in prd:
        p.join()
    q.join()    
    


    
if __name__ == '__main__':
    main()    