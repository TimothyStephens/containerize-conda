# Containerize Bakta

## v1.9.1 (database version 5)

### Revision 1

```
program="Bakta"
version="1.9.1"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}
conda activate ${conda_env}
bakta_db download --type full 1>download.log 2>&1
chown -R root db
mv db ${conda_env}/data/
conda env config vars set BAKTA_DB=${conda_env}/data/db

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif bakta --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



