import pandas as pd
import numpy as np

''' 
    We store the Lattice in the form of list, each item (distance) in the form of a vector
    Initialization of Lattice 
    without which the list is empty and we can NOT add elements to the list due to 'list index out of range'
'''
Lattice = [{(0,0,0,0)},{(0,0,0,0)},{(0,0,0,0)},
    {(0,0,0,0)},{(0,0,0,0)},{(0,0,0,0)},
    {(0,0,0,0)},{(0,0,0,0)},{(0,0,0,0)}]

'''
    Note that each element in the tuple is set in the formulation of 
    (Layer_sex,Layer_race,Layer_marital_status,Layer_age)
    each with the layer of 0-1, 0-1, 0-2, 0-4 
    layer = 0 means data is not generalized, layer = top means the attribute is generalized to *
'''
for Layer_sex in range(2):
    for Layer_race in range(2):
        for Layer_marital_status in range(3):
            for Layer_age in range(5):
                Lattice[Layer_age + Layer_marital_status + Layer_race + Layer_sex].add((Layer_sex,Layer_race,Layer_marital_status,Layer_age))

'''
    We delete (0,0,0,0) of Lattice[1:9], which was introduced just to make the initialization job
    and by doing so we have the final Lattice
 '''
for i in range(8):
    Lattice[i + 1].remove((0,0,0,0))

print(Lattice)

'''
    We proceed to traverse every set (element of Lattice)
    Note: There is no index of set in Python
'''

for vector in Lattice[3]:
    print(vector)
