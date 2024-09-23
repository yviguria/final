"# Agonist-Antagonist" 
Scripts Details:

cavity_find_pocket.bash : This bash script finds the pocket around the given ligand using ligbuilder.

extract_chain.py: Extract only those chains from the pdb file in which ligand is present.

fpocket_find_pocket.bash: This bash script finds the pocket around the givcen ligand using fpocket.

ml_training.ipynb: This juypter notebook trains the various machine learning models and evaluate those models.

temp_parse_files.ipynb: This juypter notebook is used to parse the text files as and ehen required.

compile_1.py, compile_2.py, and compile_3.bash : Given a pdb name and ligand, these scripts file extract features from ligbuilder and fpocket, and predicts the sample using the saved machine learning model.

To find if the given pdb and ligand is agonist or antagonist, go to Predict_Sample directory and run the command "python3 compile_1.py" from the bash terminal.
