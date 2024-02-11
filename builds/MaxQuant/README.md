# Containerize MaxQuant

## v2.4.13.0

### Revision 1

```
program="MaxQuant"
version="2.4.13.0"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c conda-forge mono=6.12.0.90
conda activate ${conda_env}

# Unpack MaxQuant and move to conda env
unzip MaxQuant_v_2.4.13.0.zip
mv MaxQuant_v_2.4.13.0 ${conda_env}/share/

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif maxquant
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



