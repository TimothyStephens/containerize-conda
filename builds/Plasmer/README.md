# Containerize Plasmer

## 23.04.20

### Revision 1

```
program="Plasmer"
version="23.04.20"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c iskoldt -c bioconda -c conda-forge -c defaults ${program}=${version}

mkdir ${conda_env}/data
cd ${conda_env}/data
wget https://zenodo.org/records/7030675/files/customizedKraken2DB.tar.xz?download=1
wget https://zenodo.org/records/7030675/files/plasmerMainDB.tar.xz?download=1

mv 'customizedKraken2DB.tar.xz?download=1' 'customizedKraken2DB.tar.xz'
mv 'plasmerMainDB.tar.xz?download=1' 'plasmerMainDB.tar.xz'

tar xf customizedKraken2DB.tar.xz
tar xf plasmerMainDB.tar.xz

rm customizedKraken2DB.tar.xz plasmerMainDB.tar.xz

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif Plasmer -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



