""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
from numba import njit
import multiprocessing
import concurrent.futures as future

# Exc1
def approximate_pi(n):
    # n is the number of points

    # Write your code here

    hit_list_x=[]
    hit_list_y=[]
    miss_list_x= []
    miss_list_y= []
    for _ in range(n):
        random_x= random.uniform(-1,1) #change x variable for each turn
        random_y= random.uniform(-1,1) # same for y
        if ((random_x**2)+(random_y**2)) <=1: #test if inside circle
            hit_list_x.append(random_x) #create list with hits, separate x and y for later plotting
            hit_list_y.append(random_y)
        else:
            miss_list_x.append(random_x,) #create list with misses
            miss_list_y.append(random_y)
    pi_result=4*(len(hit_list_x))/(len(miss_list_x)+len(hit_list_x)) #denominator same as n
    #plotting
    plt.figure(figsize=(6,6))
    plt.scatter(hit_list_x,hit_list_y,color='red',s=2)
    plt.scatter(miss_list_x,miss_list_y, color='blue',s=2)
    plt.show()
    plt.savefig(f'approximate_pi_for_n={n}')
    #do for n={1000,10000,100000}

    return pi_result 

        

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points

    # d is the number of dimensions of the sphere 

    points_list= [[random.uniform(-1,1) for _ in range(d)] for _ in range(n)]
   # hit_counter=0
    #for list_element in points_list:
        #if sum(list(map(lambda x: x**2, list_element))) <=1:
          #  hit_counter+=1
    hit_list=list(filter(lambda x: sum(map(lambda y: y**2, x)) <=1, points_list))
    #x is each element in points list which is a list with d elements
    return  (2**d)*len(hit_list)/n

#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    return (m.pi**(d/2))/m.gamma((d*0.5)+1)
"""n=100000
for d in [2, 11]:
    print(sphere_volume(n, d))
    print(hypersphere_exact(n, d))"""
#testing time it takes to run sphere_volume
"""start = pc()
sphere_volume(10**6, 11)
end = pc()
print(end-start)
start = pc()
sphere_volume(10**6, 11)
end = pc()
print(end - start)

start = pc()
sphere_volume(10**6, 11)
end = pc()
print(end - start)"""
#Results were: 2.266627073287964 s,
#2.2614920139312744 s, 
#2.1931869983673096 s.

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points

    # d is the number of dimensions of the sphere
    #np is the number of processes
    hit_counter=0

    for _ in range(n):
        sum=0 #creating a variable for every iteration, if the sum of the random squares are less than one we add to hit_counter
        for __ in range(d):
            variable=random.uniform(-1,1) #one random coordinate for each dimension
            sum+=variable**2
        if sum<=1: #checking each sum if it is larger than 1
            hit_counter+=1
    
    
    return (2**d)*hit_counter/n
#testing time it takes to run sphere_volume_numba
"""start = pc()
sphere_volume_numba(10**6, 11)
end = pc()
print(end-start)
start = pc()
sphere_volume_numba(10**6, 11)
end = pc()
print(end - start)

start = pc()
sphere_volume_numba(10**6, 11)
end = pc()
print(end - start)"""
#Results were: 0.3025338649749756,
#0.024585962295532227,
#0.024487972259521484. Clear improvement in the last two runs compared to the first
#Numba was much faster and had better performance

#Exc4: parallel code - parallelize actual computations by splitting data

def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes

    # n is the number of points

    # d is the number of dimensions of the sphere 
    n_processes=4
    n_per_process= n //n_processes

    with future.ProcessPoolExecutor() as ex:
        hits_per_process = ex.map( sphere_volume, [n_per_process] * n_processes, [d]* n_processes)
# future.ProcessPoolExecutor() as ex creates a pooled executor which can basically execute code simultaneously
# ex.map expects a function (sphere_volume) and then what parameters to feed the different executors
# Since we then give two separate list the executor will execute the function:
# The first ex first parameter will be the first element of the first list, the second parameter will be the first element of the second list
# map then pools the results as a list of what the executors returned for their execution
    return sum(hits_per_process)/ n_processes 
# since we got 4 different volume calculations we sum them and divide by number of processors to get the mean of the parallell calculation

    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    print("What is numba time?")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    start = pc()
    sphere_volume_parallel(n,d)
    stop = pc()
    print(f'Exc4: Parallell time of {d} and {n}: {stop-start}')
    print("What is parallel time?")

    
    
if __name__ == '__main__':
	main()

