
from pathlib import Path
import pandas as pd
import os
from Bio import PDB
from Bio.PDB.PDBParser import PDBParser
import numpy as np
import urllib.request

## Extract chain
class ChainSplitter:
    def __init__(self, out_dir=None):
        """ Create parsing and writing objects, specify output directory. """
        self.parser = PDB.PDBParser()
        self.writer = PDB.PDBIO()
        if out_dir is None:
            out_dir = os.path.join(os.getcwd(), "chain_PDBs")
        self.out_dir = out_dir

    def make_pdb(self, pdb_path, chain_letters, out_name, overwrite=True, struct=None):
        """ Create a new PDB file containing only the specified chains.

        Returns the path to the created file.

        :param pdb_path: full path to the crystal structure
        :param chain_letters: iterable of chain characters (case insensitive)
        :param overwrite: write over the output file if it exists
        """
        chain_letters = [chain.upper() for chain in chain_letters]

        # Input/output files
        (pdb_dir, pdb_fn) = os.path.split(pdb_path)
        pdb_id = pdb_fn[0:4]
        print(out_name)
        out_path = os.path.join(self.out_dir, out_name)
        print("OUT PATH:",out_path)
        plural = "s" if (len(chain_letters) > 1) else ""  # for printing

        # Skip PDB generation if the file already exists
        if (not overwrite) and (os.path.isfile(out_path)):
            print("Chain%s %s of '%s' already extracted to '%s'." %
                    (plural, ", ".join(chain_letters), pdb_id, out_name))
            return out_path

        print("Extracting chain%s %s from %s..." % (plural,
                ", ".join(chain_letters), pdb_fn))

        # Get structure, write new file with only given chains
        if struct is None:
            struct = self.parser.get_structure(pdb_id, pdb_path)
        self.writer.set_structure(struct)
        self.writer.save(out_path, select=SelectChains(chain_letters))

        return out_path


class SelectChains(PDB.Select):
    """ Only accept the specified chains when saving. """
    def __init__(self, chain_letters):
        self.chain_letters = chain_letters

    def accept_chain(self, chain):
        return (chain.get_id() in self.chain_letters)

print('started')


pdbList = PDB.PDBList()
splitter = ChainSplitter("")  # Change me.
# pdb_id = '6pt0'
pdb_id = input("Enter pdb Id ")
pdb_fn =   pdb_id + '.pdb'
urllib.request.urlretrieve('http://files.rcsb.org/download/' + pdb_fn, pdb_fn)
structure = PDBParser().get_structure(pdb_fn, pdb_fn) 
model = structure[0]
# WI5'
lig = input("Enter Ligand : ").upper()
chain = 'NA'
list_chains = []
for i in model.get_residues():
    if(i.get_resname() == lig):
        list_chains.append(str(i.get_parent())[10 : -1])
list_chains.sort()
if(len(list_chains) == 0) : print('could not seperate chain')
else:
    chain = list_chains[0]
    output_name = 'pdb' + pdb_id + '_' + lig + '.ent'
    splitter.make_pdb(pdb_fn, chain, output_name)


## Modifying dpocket
file_dpocket = open("test_dpocket.txt", "w")
line = 'pdb' + pdb_id + '_' + lig + '.ent ' + lig + '\n'
file_dpocket.writelines(line)
file_dpocket.close()
print(line)

import subprocess
## Run dpocket -f test_dpocket.txt
# print("fpocket started")
bashCommand = "./dpocket -f test_dpocket.txt"
process = subprocess.Popen("./dpocket -f test_dpocket.txt", shell = True)
output, error = process.communicate()

# obabel *.pdb -omol2 -m

from pathlib import Path
import pandas as pd

protein = pdb_id
path1 = Path('pdb' + protein.lower() + "_" + lig + ".ent")
file1 = open(path1, 'r')
Lines = file1.readlines()
message = []
for line in Lines:
    if(lig in line):
        message.append(line)
    ## list_of_words = line.split()
    ## for words in list_of_words:
    ##     if words == lig and list_of_words[0][0:6] == "HETATM":
    ##         message.append(line)
    ##         break
save_file = Path(protein + "_" + lig + '_ligand' + ".pdb")
with open(save_file, 'w') as file:
    file.writelines(message)

print('fpocket end')

## Run openbabel command
print('openbabel started')
import subprocess
bashCommand = "obabel *ligand.pdb -omol2 -m"
process = subprocess.Popen("obabel *ligand.pdb -omol2 -m", shell = True)
output, error = process.communicate()
print('openbabel end')

# Run Cavity
print('cavity started')
file_cavity = open('PDB_ligand_file_1.txt', 'w')
line = 'pdb' + pdb_id + '_' + lig + '.ent ' + pdb_id + '_' + lig + '_' + 'ligand.mol2\n'
file_cavity.writelines(line)
process = subprocess.Popen("./abc_script.bash", shell = True)
file_cavity.close()
print("cavity end")


# Extracting Features
# def isPositive(feat,read):
#     # line2 = read[1].split()
#     if len(read)>1:
#         line1 = read[0].split()
#         line2 = read[1].split()
#         # if len(line2)>0:
#         #     list_temp.append(line2)
#     else:
#         return np.nan
#     #print('count', len(feat))
#     percent = 0
#     count = 0
#     for i in range(1, 21):
#         percent = percent + feat[-i] * int(line2[-i])
#         count = count + int(line2[-i])
#     percent = percent / count

#     return percent
# def make(feat, f):
#     read = f.readlines()
#     f.close()
#     line2 = read[1].split()
#     # print('count', line2[2],line2[9:])
    
#     percent = 0
#     count = 0
#     return arr

    

    
# #ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL

# # iterate through all file
# dic={}
# hyd=[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
# hyd_perc=[]
# polar=[0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
# polar_perc = []
# aromatic = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
# aromatic_perc = [] 
# aliphatic = [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 , 0, 1]
# aliphatic_perc=[]
# small=[1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
# small_perc=[]
# for file in os.listdir():
# 	# Check whether file is in text format or not
#     if file.endswith("dpout_fpocketp.txt"):
#         file_path = file

#         # call read text file function
#         # read_text_file(file_path)
#         f = open(file_path, 'r')
#         read = f.readlines()
#         arr =[]
#         #print(read)
#         if len(read)>1:
#             read1 = read[1].split()
#             arr.append(read1[2])
#             for i in range(len(read1)):
#                 #print(i,read1[i])
#                 if i > 8 and i<31 or i>36: 
#                     arr.append(read1[i])
            
#             arr.append(isPositive(hyd, read))
#             arr.append(isPositive(polar, read))
#             arr.append(isPositive(aromatic, read))
#             arr.append(isPositive(aliphatic,read))
#             arr.append(isPositive(small,read))
            
            
#             for i in range(len(arr)):
#                 if arr[i] == "#NAME?":
#                     arr[i] = 1
#             #print(len(arr))
            
#             f.close()

# # def read_text_file(file_path):
# # 	with open(file_path, 'r') as f:
# # 		print(f.read())
# def isPositive1(read):
#     # line2 = read[1].split()
#     x = 36
#     if read[36].split()[5] == 'closed,':
#         x = x+1
#     return x

    

    
# #ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL

# # iterate through all file
# dic={}
# i = 0
# name = []
# surface_area = []
# maximal_pkd = []
# average_pkd = []
# drugscore = []
# druggability = []

# i = 0
# arr2 = []
# for file in os.listdir():
# 	# Check whether file is in text format or not
#     if file.endswith("surface_1.pdb"):
#         file_path = file

#         # call read text file function
#         # read_text_file(file_path)
#         f = open(file_path, 'r')
#         read = f.readlines()
#         name.append(file_path[:-14])
#         ct = isPositive1(read)   
#         arr.append(read[16].split()[6])
#         arr.append(read[ct].split()[5])
#         arr.append(read[ct+1].split()[5])
#         arr.append(read[ct+2].split()[4])
#         temp = read[ct+3].split()[3]
#         if temp == 'Druggable':
#             arr.append(1)
#         else:
#             arr.append(0)
#         f.close()
# print(len(arr))

# arr = np.array(arr)
# print('hello')

# ### Applying ML model
# import pickle
# load_model = pickle.load(open('ML_Model.sav', 'rb'))
# print('hi ')
# print(load_model.predict(arr.reshape(-1, arr.shape[0])))



