from pathlib import Path
import pandas as pd
import os
from Bio import PDB
from Bio.PDB.PDBParser import PDBParser
import numpy as np
import math

# Extracting Features
def isPositive(feat,read):
    # line2 = read[1].split()
    if len(read)>1:
        line1 = read[0].split()
        line2 = read[1].split()
        # if len(line2)>0:
        #     list_temp.append(line2)
    else:
        return np.nan
    #print('count', len(feat))
    percent = 0
    count = 0
    for i in range(1, 21):
        percent = percent + feat[-i] * int(line2[-i])
        count = count + int(line2[-i])
    percent = percent / count

    return percent
def make(feat, f):
    read = f.readlines()
    f.close()
    line2 = read[1].split()
    # print('count', line2[2],line2[9:])
    
    percent = 0
    count = 0
    return arr

    

    
#ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL

# iterate through all file
dic={}
hyd=[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
hyd_perc=[]
polar=[0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
polar_perc = []
aromatic = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
aromatic_perc = [] 
aliphatic = [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 , 0, 1]
aliphatic_perc=[]
small=[1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
small_perc=[]
for file in os.listdir():
	# Check whether file is in text format or not
    if file.endswith("dpout_fpocketp.txt"):
        file_path = file

        # call read text file function
        # read_text_file(file_path)
        f = open(file_path, 'r')
        read = f.readlines()
        arr =[]
        #print(read)
        if len(read)>1:
            read1 = read[1].split()
            arr.append(read1[2])
            for i in range(len(read1)):
                #print(i,read1[i])
                #if i > 8 and i<31 or i>36: 
                if i > 8: 
                    arr.append(read1[i])
            arr.append(isPositive(hyd, read))
            arr.append(isPositive(polar, read))
            arr.append(isPositive(aromatic, read))
            arr.append(isPositive(aliphatic,read))
            arr.append(isPositive(small,read))
            

            for i in range(len(arr)):
                if arr[i] == "#NAME?" or arr[i] == '-nan' or arr[i] == 'nan':
                    arr[i] = 1
            #print(len(arr))
            
            f.close()
# def read_text_file(file_path):
# 	with open(file_path, 'r') as f:
# 		print(f.read())
def isPositive1(read):
    # line2 = read[1].split()
    x = 36
    if read[36].split()[5] == 'closed,':
        x = x+1
    return x

    
    
#ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL

# iterate through all file
dic={}
i = 0
name = []
surface_area = []
maximal_pkd = []
average_pkd = []
drugscore = []
druggability = []

i = 0
arr2 = []
for file in os.listdir():
	# Check whether file is in text format or not
    if file.endswith("_surface_1.pdb"):
        file_path = file
        
        print(file_path)
        # call read text file function
        # read_text_file(file_path)
        f = open(file_path, 'r')
        read = f.readlines()
        name.append(file_path[:-14])
        ct = isPositive1(read)   
        arr.append(read[16].split()[6])
        arr.append(read[ct].split()[5])
        arr.append(read[ct+1].split()[5])
        arr.append(read[ct+2].split()[4])
        temp = read[ct+3].split()[3]
        if temp == 'Druggable':
            arr.append(1)
        else:
            arr.append(0)
        f.close()

# for i in range(len(arr)):
#     if arr[i] == "#NAME?" or math.isnan(arr[i]):
#         arr[i] = 1
arr = np.array(arr)

### Applying ML model
import pickle
load_model = pickle.load(open('ML_Model.sav', 'rb'))
print(load_model.predict(arr.reshape(-1, arr.shape[0])))


for file in os.listdir():
	# Check whether file is in text format or not
    if file.endswith("ent") or file.endswith("pdb") or file.endswith("mol2") or file.endswith('fpocketp1.txt'):
        file_path = file
        os.remove(file_path)
print("ended")