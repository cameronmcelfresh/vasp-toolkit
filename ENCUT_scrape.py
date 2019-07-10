# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:55:26 2019

@author: Cameron
"""

"""The program prompts the user to select a directory that holds output files from DFT 
simulations in VASP. This program will locate the resulting final TOTEN
minimization energy from a given respective trial, and link it to the ENCUT value provided
in the correlated INCAR file (must be in the same folder). After going through all folders 
contianing an INCAR and OUTCAR file, this program will print the plot the 
ENCUT and minimum TOTEN value for each trial"""

"""Find the directory of the file containing all of the individual VASP Trials
 - Do this through user selection"""
 
from tkinter import filedialog
from tkinter import *
import os
import re
import matplotlib.pyplot as plt

root = Tk()
root.directory =  filedialog.askdirectory(title = 'Select the file that contains all of the VASP trial folders') #Extract the base directory using tk
#The base directory is the folder that holds all of the individual VASP trail folders with 
#their respective INCAR, OUTCAR, POSCAR, etc. files

#Create empty lists to hold both the ENCUT values and the final TOTEN values
encut_vals = []
toten_vals = []

#Loop through the directories holding individual VASP experimental trials
for test_dir in os.listdir(root.directory):
    
    #Ensure that both INCAR and OUTCAR files exist in the directory
    outcar_path =root.directory +'/' +  test_dir +'/OUTCAR'
    incar_path = root.directory + '/' + test_dir +'/INCAR'
    
    """If an OUTCAR or INCAR file does not exist in the folder, skip directory"""
    if os.path.exists(incar_path) and os.path.exists(outcar_path):
        
        encut_val = 0 #Initialize the ENCUT and TOTEN values
        toten_val = 0
        
        """Extract the encut_val (ENCUT value)"""
        file= open(incar_path, 'rt')
        for line in file:
            if "ENCUT" in line: #Find the ENCUT entry line
                
                encut_val = int(re.sub('[^0-9]','',line)) #Extract the ENCUT value from the INCAR file
                print('\nEncut_val: ' + str(encut_val)) #Print for visualization
                
        file.close()
        
        """Extract the encut_val (TOTEN value)"""
        file= open(outcar_path, 'rt')
        for line in file:
            if "TOTEN" in line: #Find the ENCUT entry line
                
                #toten_val = int(re.sub('[^0-9]','',line)) #Extract the TOTEN value from the INCAR file
                line_val = line[25:-3]
                
                #Assign the toten_val variable
                toten_val = float(line_val.strip())
                
                #Print so the data can be visualized during extraction
                print('Toten_val: ' + str(toten_val)[:7])
        file.close()
        
        """Append the encut and toten values to the final lists to hold the values"""
        if encut_val != 0 and toten_val !=0 :
            
            #Only do this action if encut_and toten have been updated (won't occur for failed VASP 
            #trails that do not update TOTEN)
            encut_vals.append(encut_val)
            toten_vals.append(toten_val)
                

if encut_vals == [] and toten_vals ==[]: 
    print('This directory does not contain the necessary VASP data! Try another one')
    
else:
    print("ENCUT\tTOTEN")
    for i in range(len(toten_vals)):
        print(str(encut_vals[i])+ '\t' + str(toten_vals[i])[:7])
        
    """Plot the ENCUT vs. TOTEN Data"""
    plt.plot(encut_vals, toten_vals, '-o')
    plt.xlabel('ENCUT')
    plt.ylabel('TOTEN (eV)')
    plt.title('ENCUT vs. TOTEN')
        
 
