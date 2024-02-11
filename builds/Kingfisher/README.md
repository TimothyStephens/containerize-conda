# Containerize Kingfisher

## v0.4.1

### Revision 1

```
program="Kingfisher"
version="0.4.1"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}
$mamba install -y -p ${conda_env} python=3.7

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif kingfisher get --full-help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



