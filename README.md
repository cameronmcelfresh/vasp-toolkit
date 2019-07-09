# vasp
Toolkit for analyzing the output files and generating the input files for VASP density functional theory simulations.


## Getting Started

The following programs are used to generate and evaluate some of the basic files used in our VASP modeling:

- POSCAR_generator.py
- NEB_image_generator.py
- ENCUT_generate.py
- ENCUT_scrape.py

A basic understanding of the POSCAR, INCAR, POTCAR, KPOINTS, and OUTCAR files is necessary. Please read through the VASP wiki on these topics and the file formats if you have not already done so. https://cms.mpi.univie.ac.at/wiki/index.php/The_VASP_Manual


## Installing
These programs utilize the following libraries:
- tikinter
- os
- shutil
- numpy
- re
- matplotlib


### POSCAR_generator
This program generates a POSCAR file with calculated atomic positions when provided the crystal structure type, repeating cell size, and lattice parameter. Currently, POSCAR_generator is developed to handle simple cubic (sc), body-centered cubic (bcc), and face-centered cubic (fcc) crystal types. 

#### Input
If the user defines the following variables in the first several lines of the code:

element = "W"
atomic_structure = "bcc"
lattice_parameter = 3.22
box_size = 2

#### Output
A POSCAR file is created in the same directory as the the current directory as the POSCAR_generator.py file. The file reads:

W bcc\
6.44\
1 0 0\
0 1 0\
0 0 1\
16\
Direct\
0.0 0.0 0.0\
0.0 0.0 0.5\
0.0 0.5 0.0\
0.0 0.5 0.5\
0.25 0.25 0.25\
0.25 0.25 0.75\
0.25 0.75 0.25\
0.25 0.75 0.75\
0.5 0.0 0.0\
0.5 0.0 0.5\
0.5 0.5 0.0\
0.5 0.5 0.5\
0.75 0.25 0.25\
0.75 0.25 0.75\
0.75 0.75 0.25\
0.75 0.75 0.75

The correct structure can then be validated by opening the newly generated POSCAR file in VESTA. 

<img src="https://github.com/cameronmcelfresh/vasp-toolkit/blob/master/w_cell.JPG" width="600">

The above picture confirms an 2x2x2 FCC structure. 

### NEB_image_generator

#### Input

#### Output

### ENCUT_generate

#### Input

#### Output

### ENCUT_scape

#### Input

#### Output




  
