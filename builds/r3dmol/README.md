# Containerize r3dmol

## v0.1.2

### Revision 1

```bash
program="r3dmol"
version="0.1.2"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def 

singularity exec ${prefix}.sif pdb_plot --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```

### Revision 2

```bash
program="r3dmol"
version="0.1.2"
revision="2"
prefix="${program}_v${version}-rev${revision}"

singularity build --sandbox ${prefix} /scratch/singularity/ColabFold_v1.5.5_cuda_v12.1.0-rev2.sif

rm r3dmol_v0.1.2-rev2/usr/local/envs/colabfold/bin/colabfold_*
cp /home/timothy/GitHub/ColabFold_Utils/pdb_plot.py r3dmol_v0.1.2-rev2/usr/local/envs/colabfold/bin/pdb_plot
chmod +x r3dmol_v0.1.2-rev2/usr/local/envs/colabfold/bin/pdb_plot
grep -A 10000 '%help' r3dmol_v0.1.2-rev1.def | grep -v '%help' | sed -e 's@-rev1.sif@-rev2.sif@' > r3dmol_v0.1.2-rev2/.singularity.d/runscript.help 

singularity build --fakeroot --force ${prefix}.sif ${prefix}

singularity exec ${prefix}.sif pdb_plot --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```

