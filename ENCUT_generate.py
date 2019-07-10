# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:55:16 2019

@author: Cameron
"""

"""This program generates the datafiles and directories to run a series of DFT simulations
using VASP software. The program requires user selection of a directory, from which
all of the POSCAR, INCAR, KPOINTS, and POTCAR files will be copied. INCAR is the only REQUIRED
file for this program to run - although it is strongly recommended that POSCAR/INCAR/POTCAR/RUN_VASP
are simultaneously copied to maintain continuity.

Procedure:
    1) Run program
    2) Select the directory which contains the required starting files (INCAR, etc.)
    3) Select the destination which will hold the directory/files
    3) As prompted, enter the min, max, and number of ENCUT values to be simualted
        For example if the following is entered:
            ENCUT min = 50
            ENCUT max = 250
            Number of ENCUT values = 5
            
            The program will generate data for trials where ENCUT = 50,100,150,200,250
            
    4) As prompted, enter the desired prefix of the directories to be created
        For example, if the following is entered:
            Directory Prefix = Tungsten2x2x2 the program will generate
                Tungsten2x2x2ENCUT50
                Tungsten2x2x2ENCUT100
                Tungsten2x2x2ENCUT150
                Tungsten2x2x2ENCUT200
                Tungsten2x2x2ENCUT250
                
            Each of these folders will contain the INCAR/POSCAR etc. files provided,
            with an pdated encut value"""


from tkinter import filedialog
from tkinter import *
import os
import shutil
import numpy as np

"""Prompt user to select the directory that contains the starting files"""

root = Tk()
root.directory =  filedialog.askdirectory(title = "Select the directory that contains the original starting files")

"""Ensure that an INCAR file is contained in the directory"""
if not(os.path.exists(root.directory + '/INCAR')):
    print("Sorry, this directory does not contain an INCAR file!")
    print("Exiting the program")

    exit()
    
"""Check for the other deisred starting files"""
desired_files = ['INCAR', 'POSCAR', 'KPOINTS', 'RUN_VASP.sh']
missing_files = []

for file_name in desired_files:
    if not(os.path.exists(root.directory + '/' + file_name)):
        missing_files.append(file_name)

#If files are missing, print the missing files for the user        
if missing_files != []:
    print("This directory is missing the following starting file(s):")
    
    for file_name in missing_files:
        print(file_name)
    
    #Provide the user with a way to exit the program if the starting directory is missing files
    ans = []

    while ans not in ['y', 'Y', 'n', 'N']:       
        ans = input("\nAre you sure you would like to continue? [Y]es or [N]o: ")
    
    if ans in ['n', 'N']: #IF the user chooses not to continue then exit the program
        exit()
        
"""Request a destination directory"""

dest = Tk()
dest.directory = filedialog.askdirectory(title = "Select the destination directory")


"""Prompt the user to enter the minimum and maximum ENCUT values"""

satisfaction = False #Set satisfaction to false

while not(satisfaction):
    
    #Request input from user
    try:
        encut_min = int(input("Please enter ENCUT minimum: "))
        encut_max = int(input("Please enter ENCUT maximum: "))
        num_encut = int(input("Please enter the number of encut values to make: "))
    except:
        print("\nSorry, please enter proper integer values!\n")

        
    
    if isinstance(encut_min, int) and isinstance(encut_max, int): #Ensure that they are integers
        if encut_min<encut_max:
            if encut_min>0 and encut_max>0: #Check for the proper ordering of values
                
                satisfaction = True #If all satisfied, set to true
                 
                encut_vals = np.linspace(encut_min, encut_max, num_encut) #Set the encut values
                
    if satisfaction==False:
        print("\nSorry, please enter proper integer values!\n")
        
    #Check to see if the values are acceptable to the user
    if satisfaction == True:
        print("You will make encut values:")
        
        for i in range(len(encut_vals)):
            print(str(int(encut_vals[i])))
            
        user_ans = input("\nAre you satisfied with these values? [Y] or [N]: ")
        
        #Check to see if these values are accpetable
        if user_ans in ["n", "N", "no", "No"]:
            satisfaction = False
                
        
"""Request user input for the prefix of the new directory - then create the directories"""

dir_prefix = input("\nPlease enter the prefix for the new directory: ")

#Create the directories with the requred prefix
dest_dirs = []
for i in range(len(encut_vals)):   
    
    #Add to the new list of directories
    dest_dirs.append(os.path.join(dest.directory, dir_prefix+"encut"+ str(int(encut_vals[i]))))
    
    try:
        os.mkdir(dest_dirs[i]) #Make new directory
    except:
        print("Sorry, these is something wrong with this prefix")
        exit()
            
        
    
"""Copy over all the files excep the INCAR file in the original directory to the new directories"""
    

#Check the files and copy them over
for i in range(len(encut_vals)): #Loop through the encut vals directories
    
    for file_name in desired_files:
        
        if file_name=="INCAR": #Do not copy INCAR file, do that seperately below
            continue
        
        full_file_name = os.path.join(root.directory,file_name)
        
        if os.path.exists(full_file_name):
            shutil.copy(full_file_name, dest_dirs[i]) #Copy the individual files
            
"""Edit the INCAR files to have the required ENCUT values"""

#Loop through the INCAR files

#Assume that the ENCUT value appears in the form:

#ENCUT = 300 #This is the value etc..

for i in range(len(encut_vals)): #Loop through the ENCUT values
    
    new_file_dir = os.path.join(dest_dirs[i], "INCAR") #Only edit the INCAR files
    old_file_dir = os.path.join(root.directory, "INCAR")
    
    f = open(old_file_dir, "r") #Open the old file to read from
    
    new_file = open(new_file_dir, "w+") #Create the new file to write to
    
    
    for line in f: #Loop through all the lines
        
        #New line to be editted
        line
        
        if "ENCUT" in line:
            start_pos = line.find("=") #Begin the "=" symbol
            end_pos = line.find("#") #End the search with "#"
                                 
            #Replace the area between the "=" and "#" with the new encut values
            my_string = " "+str(int(encut_vals[i]))+" "            

            
            new_file.write(line[:start_pos+1]) #Write proceeding text
            new_file.write(my_string)  #Add in new text
            new_file.write(line[end_pos-1:]) #Add in the trailing text
        
        if not("ENCUT" in line):
            new_file.write(line) #Write the new line
            
            
    f.close() #Close the file
    new_file.close() #Close the newly written file

    
