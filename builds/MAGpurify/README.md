# Containerize MAGpurify

## v2.1.2

### Revision 1

```
program="MAGpurify"
version="2.1.2"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}
conda activate ${conda_env}
mkdir -p ${conda_env}/data; cd ${conda_env}/data/
wget https://zenodo.org/record/3688811/files/MAGpurify-db-v1.0.tar.bz2
tar -xf MAGpurify-db-v1.0.tar.bz2
rm MAGpurify-db-v1.0.tar.bz2
chown -R root:root MAGpurify-db-v1.0
chmod -R 755 MAGpurify-db-v1.0
conda env config vars set MAGPURIFYDB=${conda_env}/data/db/MAGpurify-db-v1.0
# May have to manually edit:
# $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif magpurify -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



