# Containerize GUNC

## v1.0.6

### Revision 1

```
program="GUNC"
version="1.0.6"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}
conda activate ${conda_env}
mkdir -p ${conda_env}/data
gunc download_db -db progenomes ${conda_env}/data
gunc download_db -db gtdb ${conda_env}/data
conda env config vars set GUNC_DB=${conda_env}/data
# May have to manually edit:
# $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif gunc --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



