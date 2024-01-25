# Containerize MAGI2 (my modified version)

## 2.0.5

### Revision 1

```
program="MAGI2"
version="2.0.5"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba env create -p ${conda_env} -f ${prefix}.env.yml
cd ${conda_env}/lib
git clone https://github.com/TimothyStephens/magi.git
cd magi/
python setup_magi2.py
cp /home/timothy/programs/ncbi-blast-2.13.0+/bin/{blastp,makeblastdb} workflow/blastbin/

cd ${conda_env}/bin
ln -s ../lib/magi/workflow_2/magi2.sh

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif magi2.sh -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



