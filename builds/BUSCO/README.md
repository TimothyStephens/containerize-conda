# Containerize BUSCO

## v5.6.1

### Revision 1

```
program="BUSCO"
version="5.6.1"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}
conda activate ${conda_env}

# Add PYTHONPATH and change shabang in 'busco' bin script
conda env config vars set PYTHONPATH=${conda_env}/lib/python3.7/site-packages
# May have to manually edit:
# $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

# Download all lineage files
mkdir ${conda_env}/data; cd ${conda_env}/data
busco --download all

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif busco --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



