# Containerize PLASMe

## 1.1

### Revision 1

```
program="PLASMe"
version="1.1"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

git clone https://github.com/HubertTang/PLASMe.git
cd PLASMe
$mamba env create -p ${conda_env} -f plasme.yaml
conda activate ${conda_env}

python PLASMe_db.py
chmod +x *.py
# Add shebang to top of each file
# Replace line 512: plasme_work_dir_path = os.getcwd()
# with: plasme_work_dir_path = "/opt/conda/envs/PLASMe_v1.1-rev1/share/PLASMe"
# to prevent isses with the script finding the database we just downloaded.
cd ../
mv PLASMe ${conda_env}/share/

cd ${conda_env}/bin
ln_loop ../share/PLASMe/*.py

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif PLASMe.py -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



