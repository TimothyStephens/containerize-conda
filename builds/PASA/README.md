# Containerize PASA

## v2.5.3

### Revision 1

```
program="PASA"
version="2.5.3"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=${version}
cd ${conda_env}
mkdir data
cd data
wget https://ftp.ncbi.nlm.nih.gov/pub/UniVec/UniVec -O UniVec.fa
wget https://ftp.ncbi.nlm.nih.gov/pub/UniVec/UniVec_Core -O UniVec_Core.fa

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif Launch_PASA_pipeline.pl -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



