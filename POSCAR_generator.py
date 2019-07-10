# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:37:10 2019

@author: Cameron
"""

"""Program to generate the .txt files that are fed into POSCAR"""



import numpy as np

"""Only change variables in this section"""

#Must use capital letter designation of element
element = "W"

#Use lower case
#Body Centered Cubic = bcc
#Face Centered Cubic = fcc
#Simple Cubic = sc
atomic_structure = "bcc"

#Constant must be in angstroms
lattice_parameter = 3.22

#Will create a 3D grid which is box_size*box_size*box_size dimensions of unit cells
#For example, if box_size = 3 we are creating a 3x3x3 grid of unit cells
box_size = 2

""" Do not change anything below this unless you wish to change the program's functionality """





"""Begin calculation for total number of atoms in the simulation and basis vectors"""
if atomic_structure =="sc":
    num_basis_atoms = 1
    
    atomic_basis = [[0,0,0], [1,0,0], [0,1,0],[0,0,1],
                    [1,0,1], [0,1,1], [1,1,1], [1,1,0]]
    
if atomic_structure =="bcc":
    num_basis_atoms = 2
    
    atomic_basis = [[0,0,0], [1,0,0], [0,1,0],[0,0,1], 
                    [1,0,1], [0,1,1], [1,1,1], [1,1,0], [0.5,0.5,0.5]]
    
if atomic_structure =="fcc":
    num_basis_atoms = 4

    atomic_basis = [[0,0,0], [1,0,0], [0,1,0],[0,0,1],
                    [1,0,1], [0,1,1], [1,1,1], [1,1,0], 
                    [0.5,0.5,0], [0, 0.5, 0.5], [0.5, 0, 0.5],
                    [0.5,0.5,1], [1, 0.5, 0.5], [0.5, 1, 0.5]]


"""Write out the total basis vectors for all atoms while also considering repeated
atoms for VASP calculations and overlapping atoms"""

#Begin by putting creating an atomic position matrix, starting with 0,0,0 point
atomic_pos = np.zeros([0,3])

shift = 1/box_size #Fraction to be added to coordinates during each iteration

#Loop through the x,y,z coordinates to produce the 3D grid of points
for z in range(box_size):        
    for y in range(box_size):         
        for x in range(box_size):
            
            new_cell = np.array(atomic_basis)*(1/box_size)+[x*shift,y*shift,z*shift]
            
            atomic_pos = np.concatenate((atomic_pos, new_cell))

#remove all repeated instances of atomic positions
atomic_pos = np.unique(atomic_pos, axis=0)

#Now remove the repeating edge atoms and leave  the unique positions

add_list = [[1,0,0], [0,1,0],[0,0,1],[1,0,1], [0,1,1], [1,1,1], [1,1,0]]

for pos in atomic_pos:
    if 0 in pos:
        for add in add_list:
            
            repeated_pos = pos+add
            
            idxs = np.any(atomic_pos !=repeated_pos , axis=1) 
            atomic_pos = atomic_pos[idxs, :]

"""Begin file generation"""

#Create the POSCAR file
file = open("POSCAR", "w")

#Generate heading
file.write(element + " " + atomic_structure + "\n")
file.write(str(lattice_parameter*box_size) + "\n")

#State the the lattice is cubic with equal spacing
file.write("1 0 0\n")
file.write("0 1 0\n")
file.write("0 0 1\n")

#Calculate and write the number of atoms that will be generated
file.write(str(box_size*box_size*box_size*num_basis_atoms) + "\n")

#Use direct coordinates as opposed to cartesian coordinates
file.write("Direct\n")

#Write out the rest of the positions
for pos in atomic_pos:
    file.write(str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + "\n")


file.close()