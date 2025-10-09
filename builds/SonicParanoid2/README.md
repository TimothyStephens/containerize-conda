# Containerize SonicParanoid2

## v2.0.9

### Revision 1

```
program="SonicParanoid2"
version="2.0.9"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} conda-forge::python==3.11 bioconda::mmseqs2==13.45111 bioconda:diamond==2.1.9 bioconda:blast==2.15.0 bioconda:mcl==14.137
$mamba activate ${conda_env}
$conda_env/bin/pip3 install --no-cache-dir sonicparanoid==2.0.9

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif sonicparanoid -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



