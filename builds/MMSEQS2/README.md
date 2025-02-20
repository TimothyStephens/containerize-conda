# Containerize MMSEQS2

## 113e3212c137d026e297c7540e1fcd039f6812b1

### Revision 1

```
program="mmseqs2"
version="113e3212c137d026e297c7540e1fcd039f6812b1"
revision="1"
prefix="${program}_${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def
singularity exec ${prefix}.sif mmseqs --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



