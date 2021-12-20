# -*- coding: utf-8 -*-

"""The program generates the required POSCAR files to run a NEB calculation on VASP

The required input files are:
    
    CONTCAR_ei (the initial position CONTCAR file)
    CONTCAR_ef (the final position CONTCAR file)
    
The user must specify the number of images (position files) desired. If both
CONTCAR_ei and CONTCAR_ef are provided and the user selects num_images = 5 then
output will be the following folders and files:
    
    00 -> POSCAR (original position from CONTCAR_ei)
    01 -> POSCAR 
    02 -> POSCAR
    03 -> POSCAR
    04 -> POSCAR
    05 -> POSCAR
    06 -> POSCAR  (final position from CONTCAR_ef)"""
    
from tkinter import filedialog
from tkinter import *
import os
import shutil
import numpy as np


# Specify the number of images to create
num_images = int(input("Enter the number of images to prepare: " ).strip())

# Calculates the number of atoms in your vasp file by reading line 7 of the provided vasp file
    # vasp_file: a string of the path to the vasp file
def number_of_atoms(vasp_file):
    f = open(vasp_file)
    lines = f.readlines()
    numbers = [int(n) for n in lines[6].split()] 
    f.close()

    return sum(numbers)


# Prompt user to select the directory that contains the starting CONTCAR files
root = Tk()
root.directory =  filedialog.askdirectory(title = 'Please select the directory which contains the CONTCAR_ei and CONTCAR_ef files')
# print(root.directory)

ei_path = root.directory + '/CONTCAR_ei'
ef_path = root.directory + '/CONTCAR_ef'

# print(ei_path)
# print(ef_path)

num_atoms = number_of_atoms(ei_path) # total number of atoms (including any interstitials)

if not(os.path.exists(ei_path)) or not(os.path.exists(ef_path)) :
    print("Sorry, this directory does not contain the required CONTCAR files!")
    print()
    print("Quitting...")
    quit()


"""Gather the interpolation data"""

# Create empty arrays to hold position data
initial_pos = np.zeros([num_atoms,3])
final_pos = np.zeros([num_atoms,3])

collect_data=0 # Binary collect data variable that begins collection of data after "Direct"
counter=0 # Instantiate a counter

# Open initial positions file
f_ei = open(ei_path, "r")

for line in f_ei:
        
    if collect_data==1:
        
        #Assign positions
        initial_pos[counter,0] = float(line.split()[0])
        initial_pos[counter,1] = float(line.split()[1])
        initial_pos[counter,2] = float(line.split()[2])
        
        counter += 1
    
    if ("Direct" in line) or ("Selective dynamics" in line):
        collect_data=1
        
    #Break out of the loop once all position data has been extracted
    if counter==num_atoms:
        
        #Reset counter and collect_data to 0
        collect_data=0
        counter=0
        
        f_ei.close() #Close file
        break


#Open final positions file
f_ef = open(ef_path, "r")

for line in f_ef:
        
    if collect_data==1:
        
        #Assign positions
        final_pos[counter,0] = float(line.split()[0])
        final_pos[counter,1] = float(line.split()[1])
        final_pos[counter,2] = float(line.split()[2])
        
        counter+=1
    
    if ("Direct" in line) or ("Selective dynamics" in line):
        collect_data=1
        
    #Break out of the loop once all position data has been extracted
    if counter==num_atoms:
        
        f_ef.close() #Close file
        break

"""Define step_vec as the linear step to be taken each iteration"""

dist_vec = (final_pos-initial_pos)/(num_images+2)


#Generate a list to hold all numpy arrays that describe the positions for all POSCAR iterations
poscars = []

#Linearly interpolate the atoms positions
for i in range(num_images+2):
    poscars.append(initial_pos + i*dist_vec)


"""Write the new files to the 00 01 02 03 ...etc image folders"""

#Loop through each image POSCAR file
for i in range(num_images+2):
    
    #Make the new directory
    dir_string = "0"+str(i)
    new_dir = os.path.join(root.directory, dir_string)
    
    try:
        os.mkdir(new_dir)
    except:
        print("Directory " + new_dir.split("\\")[-1] + " already exists. Quitting...")
        quit()
    
    #Create, and begin writing to new POSCAR file
    new_file = open(new_dir+"/POSCAR", "w")
    
    #Open the initial position file 
    f_ei = open(ei_path, "r")
    
    #Use counter and data_write
    counter = 0
    data_write = 0 #Binary [0] don't write and [1] write
    
    for line in f_ei:
        
        
        #For when we are copying from the original file
        if data_write ==0:
            new_file.write(line) #Write new line to POSCAR file
        
        #For when we are writing from our newly calculated data
        if data_write==1:
            
            #Extract the position of interest for the respective atoms
            position = poscars[i][counter]
            
            #Write new lines
            #Keep in mind proper spacing and trailing zeros as traditional POSCAR files have
            new_file.write(format(position[0],'3.16f').rjust(20))
            new_file.write(format(position[1],'3.16f').rjust(20))
            new_file.write(format(position[2],'3.16f').rjust(20)+'\n')
            
            #Increase counter
            counter+=1
            
            #When the counter reaches the number of atoms stop writing new data
            if counter == num_atoms:
                data_write=0
            
        #Flags to catch the "Direct" line
        if ("Direct" in line) or ("Selective dynamics" in line):
            data_write =1 #Begin writing linearly interpolated data after "Direct"
    
    #Close our files
    new_file.close()
    f_ei.close()
