# Containerize HOTSPOT

## 20240308

### Revision 1

```
program="HOTSPOT"
version="20240308"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

git clone https://github.com/Orin-beep/HOTSPOT
cd HOTSPOT/
chmod +x *.sh *.py
# Add shebang to top of each python script
$mamba env create -f environment.yaml -p ${conda_env}
conda activate ${conda_env}

sh prepare_db.sh
sh prepare_mdl.sh

mv HOTSPOT ${conda_env}/share/
cd ${conda_env}/bin
ln_loop ../share/HOTSPOT/*.py

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif HOTSPOT.py -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



