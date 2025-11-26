# Containerize MDMcleaner

## v0.8.7

### Revision 1

```
program="MDMcleaner"
version="0.8.7"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda -c conda-forge python=3.11 ${program}=${version}
#conda activate ${conda_env}
#mdmcleaner makedb -o ${conda_env}/share/mdmcleaner_database 1>download.log 2>&1
#mdmcleaner set_configs --db_basedir ${conda_env}/share/mdmcleaner_database

python conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif mdmcleaner --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



