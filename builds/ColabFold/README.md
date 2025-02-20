# Containerize ColabFold

## v1.5.5

### Revision 1

```
program="ColabFold"
version="1.5.5"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} python=3.9
conda activate ${conda_env}
cd ${conda_env}/share/
wget https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/install_colabbatch_linux.sh
bash install_colabbatch_linux.sh

# Install specific version of MMSeq2 to ensure compatability
wget https://github.com/soedinglab/MMseqs2/archive/71dd32ec43e3ac4dabf111bbc4b124f1c66a85f1.zip
unzip 71dd32ec43e3ac4dabf111bbc4b124f1c66a85f1.zip
cd MMseqs2-71dd32ec43e3ac4dabf111bbc4b124f1c66a85f1
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=. ..
make
make install 

cd ${conda_env}/bin
ln_loop ../share/localcolabfold/colabfold-conda/bin/colabfold_*
ln -s ../share/MMseqs2-71dd32ec43e3ac4dabf111bbc4b124f1c66a85f1/build/bin/mmseqs 

# Download base git repo for database setup script
git clone https://github.com/sokrypton/ColabFold.git

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif colabfold_search -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```


## v1.5.5_cuda12.1.0

### Revision 1

```bash
program="ColabFold"
version="1.5.5"
cuda_version="12.1.0"
revision="1"
prefix="${program}_v${version}_cuda_v${cuda_version}-rev${revision}"

cat ColabFold_cuda-rev${revision}.def \
  | sed -e "s/{{COLABFOLD_VERSION}}/$version/g" -e "s/{{CUDA_VERSION}}/$cuda_version/g" -e "s/{{REVISION}}/$revision/g" \
  | singularity build --fakeroot --force ${prefix}.sif /dev/stdin 
```


### Revision 2

With custom scripts for cleaning inpu
```bash
program="ColabFold"
version="1.5.5"
cuda_version="12.1.0"
revision="2"
prefix="${program}_v${version}_cuda_v${cuda_version}-rev${revision}"

cat ColabFold_cuda-rev${revision}.def \
  | sed -e "s/{{COLABFOLD_VERSION}}/$version/g" -e "s/{{CUDA_VERSION}}/$cuda_version/g" -e "s/{{REVISION}}/$revision/g" \
  | singularity build --fakeroot --force ${prefix}.sif /dev/stdin
```



