#!/bin/bash
file="PDB_ligand_file_1.txt"
file1="cavity-AA.input"
prev_pdb="abc.ent"
prev_lig="abc.mol2"
while IFS= read -r line
do
	cd /mnt/c/users/prash/desktop/biop/ip_biop/cavity/example
	line_array=($line)
	sed -i "s/$prev_pdb/${line_array[0]}/g" "$file1"
	sed -i "s/$prev_lig/${line_array[1]}/g" "$file1"
	prev_pdb=${line_array[0]}
	prev_lig=${line_array[1]}
	cd /mnt/c/users/prash/desktop/biop/ip_biop/cavity
	./cavity64 example/cavity-AA.input
	echo "over"
	#printf '%s\n' "$prev_pdb"
	#printf '%s\n' "$line"
done <"$file"
cd /mnt/c/users/prash/desktop/biop/ip_biop/cavity/example
sed -i "s/$prev_pdb/"abc.ent"/g" "$file1"
sed -i "s/$prev_lig/"abc.mol2"/g" "$file1"
echo "over"