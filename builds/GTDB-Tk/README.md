# Containerize GTDB-Tk

## v2.3.2 (database version vR214)

### Revision 1

```
program="GTDB-Tk"
version="2.3.2"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c conda-forge -c bioconda gtdbtk=${version}
conda activate ${conda_env}
download-db.sh 1>download.log 2>&1

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif gtdbtk --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



