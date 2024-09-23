
from pathlib import Path
import pandas as pd

import os
from Bio import PDB


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
""" Parses PDB id's desired chains, and creates new PDB structures. """



pdbList = PDB.PDBList()
splitter = ChainSplitter(r"C:\Users\prash\Desktop\BioP\IP_BioP\Cavity\example\AA\MyExample")  # Change me.

df = pd.read_excel(r'C:\Users\prash\Desktop\BioP\IP_BioP\pairwise_smiles.xlsx', usecols='E, I')
count = 0
for ind in df.index:
    pdb_id = df['PDB_ID'][ind].lower()
    ligands = df['COMPOUND_IDS'][ind][1 : -1].split(', ' )
    pdb_fn =  "c:/Users/prash/Desktop/BioP/IP_BioP/PDB_Files_All/" + pdb_id + '.pdb'
    file1 = open(pdb_fn, 'r')
    Lines = file1.readlines()
    for ligand in ligands:
        lig = ligand[1 : -1]
        chain = 'NA'
        list_chains = []
        for line in Lines:
            list_of_words = line.split()
            do_capture = False
            for words in list_of_words:
                if do_capture : 
                    if words == lig : continue
                    list_chains.append(words)
                    break
                if words == lig and list_of_words[0][0:6] == "HETATM":
                    do_capture = True
            # if not (chain == 'NA') : break
        list_chains.sort()
        chain = list_chains[0]
        print(pdb_id, lig, chain)
        output_name = 'pdb' + pdb_id + '_' + lig + '.ent'
        print(output_name)
        splitter.make_pdb(pdb_fn, chain, output_name)

    count += 1
    if count >= 16 : break
