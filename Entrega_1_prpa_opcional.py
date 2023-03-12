# -*- coding: utf-8 -*-
"""
Spyder Editor

Entrega 1 parte opcional

Germán Sánchez Cuesta
"""
import time
import random
from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore


NProd=5 #Número de productores
N=7 #Número de enteros que generaremos(puede ser mayor que el tamaño de los buffers, funciona por una cola ciclica)
N0=5 #Tamaño de los buffers que vamos a usar

#Productor. Recibe su índice, prob para ir aumentado los valores que se producen, el store, tres semáforos y pos para tener la última posición en la que se consumió
def producer (index,prob,storprod,full,sem_prod,pos,mutex):
    thistor=storprod[index]
    for i in range(N):
      mutex.acquire()
      d=random.randint(prob[index].value+1,prob[index].value+9)
      print(f"producer {current_process().name} produce {d}\n")  
      if thistor[i%N0]==-2:
        thistor[i%N0]=d
        print(f"producer {current_process().name} almacena {d}\n")
        prob[index].value+=9
      full.release()
      print(f"El almacen es [{muestra(storprod,0)},{muestra(storprod,1)},{muestra(storprod,2)},{muestra(storprod,3)},{muestra(storprod,4)}\n")
      mutex.release()
      sem_prod.acquire() 
    full.release()
    z=pos[index]
    z+=1
    z%=N0
    thistor[z]=-1
    
#Consumidor. Recibe el store, los tres semáforos y pos para ir almacenando el la última posición consumida de cada productor    
def consumer(stor2,full,sem,pos,mutex):
    storage=[]
    for i in range(NProd):
        full[i].acquire()
    while True in todo1neg(stor2):
     print(f"El almacen es [{muestra(stor2,0)},{muestra(stor2,1)},{muestra(stor2,2)},{muestra(stor2,3)},{muestra(stor2,4)}")
     minimo=10**8    
     for i in range(NProd):
        if stor2[i][pos[i]]> 0 and stor2[i][pos[i]]<minimo:
            minimo=stor2[i][pos[i]]
            sel=i
     storage.append(minimo)
     print (f"consumer consumiendo {minimo}\n")
     stor2[sel][pos[sel]]=-2
     pos[sel]+=1
     pos[sel]%=N0
     sem[sel].release()
     full[sel].acquire()
    print(f"El almacen final es {storage}")

#Función para parar el consumidor
def todo1neg(storage):
    val=[True]*NProd
    pos=[False]*NProd
    for a in range(NProd):
        for b in range (N0):
            if (storage[a])[b]==-1:
                val[a]=False
            if(storage[a])[b]>0:
                pos[a]=True
    return val+pos    

#Función para hacer los prints
def muestra(storage,i):
    res=[]
    for a in range(N0):
        res.append(storage[i][a])
    return res    

def main():
    pos=Array('i',NProd)
    storprod=[]
    for i in range(NProd):
        storprod.append(Array('i',N0))
    for i in range(NProd):
        for j in range(N0):
           (storprod[i])[j]=-2   
    mutex=Semaphore(1)       
    prob=[]
    full=[]
    sem=[]
    for i in range(NProd):
        sem.append(Semaphore(1))
        full.append(Semaphore(0))
        prob.append(Value('i',0))
    index=Value('i',0)
    prd=[]
    index.value=0
    for j in range(NProd):
        prd.append(Process(target=producer, name = f'prod_{j}', args = (index.value,prob, storprod, full[index.value], sem[index.value],pos,mutex)))
        index.value+=1
    q=Process(target=consumer,args=(storprod,full,sem,pos,mutex))
    for p in prd:
        p.start()  
    q.start()    
    for p in prd:
        p.join()
    q.join()    
    


    
if __name__ == '__main__':
    main()    