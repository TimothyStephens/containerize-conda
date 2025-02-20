# Containerize PlasmidHunter

## 1.3

### Revision 1

```
program="PlasmidHunter"
version="1.3"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda python=3.10 diamond=2.1.8 prodigal
conda activate ${conda_env}
${conda_env}/bin/pip install ${program}==${version}

# Run a test to force download of database.
echo -e ">a\nAAAAAAAAAATTTTTTTTTTGGGGGGGGGGCCCCCCCCCC" > test.fa
plasmidhunter -i test.fa

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif plasmidhunter -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



