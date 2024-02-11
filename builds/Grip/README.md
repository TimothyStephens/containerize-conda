# Containerize Grip

## v4.6.2

### Revision 1

```
program="Grip"
version="4.6.2"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif grip --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



