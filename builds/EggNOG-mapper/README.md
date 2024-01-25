# Containerize EggNOG-mapper

## v2.1.12 (database version v5)

### Revision 1

```
program="EggNOG-mapper"
version="2.1.12"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} bioconda::eggnog-mapper=${version}
conda activate ${conda_env}
mkdir -p ${conda_env}/lib/python3.12/site-packages/data
download_eggnog_data.py -P

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif emapper.py --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



