unified_memory = True
import os
from string import ascii_uppercase
import json
import subprocess

#@title find_symmetry
method = "make_symmdef" #@param ["AnAnaS", "make_symmdef"]

ini_pdb = f"pdb/best.pdb"

if method == "AnAnaS":
  sym_pdb = f"pdb/sym.pdb"
  sym_json = f"pdb/sym.json"

  best_rmsd = None
  best_k = None
  for k in range(2,13):
    cmd = f"./ananas {ini_pdb} c{k} -C 100"
    rmsd = float(subprocess.getoutput(cmd).split("Average RMSD")[1].split()[1])
    print(f"c{k} rmsd={rmsd:.3}")
    if best_rmsd is None or rmsd < best_rmsd:
      best_rmsd = rmsd
      best_k = k

  cmd = f"./ananas {ini_pdb} c{best_k} -C 100 --symmetrize {sym_pdb} --json {sym_json}"
  os.system(cmd)
  results = json.loads(open(sym_json,"r").read())
  group = results[0]["group"]
  rmsd = results[0]["Average_RMSD"]
  print(f"AnAnaS detected {group} symmetry at RMSD:{rmsd:.3}")

if method == "make_symmdef":
  sym_pdb = f"pdb/best_symm.pdb"
  sym_def = f"pdb/best_symm.txt"
  sym_log = f"pdb/best_symm.log.txt"
  cmd = f"perl make_symmdef_file.pl -m NCS -p {ini_pdb} 2> {sym_log} 1> {sym_def}"
  os.system(cmd)
  for line in open(sym_log,"r").readlines():
    print(line.rstrip())

#copies = !grep TER {sym_pdb} | wc -l
#copies = int(copies[0])
#print(copies)

