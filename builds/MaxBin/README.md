# Containerize MaxBin

## v2.2.7

### Revision 1

```
program="MaxBin2"
version="2.2.7"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda -c conda-forge ${program}=${version} python=3.11.4 pandas=2.0.2 tqdm=4.65.0
conda activate ${conda_env}
P=$PWD
D=$(which run_MaxBin.pl | xargs readlink -f | xargs dirname); cd $D/
patch -N < $P/${prefix}.patch
cd $P/

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif run_MaxBin.pl -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



