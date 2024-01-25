# Containerize ViralRecall

## v2.0

### Revision 1

```
program="ViralRecall"
version="2.0"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda python=3.6 prodigal hmmer biopython matplotlib numpy pandas
conda activate ${conda_env}
cd ${CONDA_PREFIX}/share
git clone https://github.com/faylward/viralrecall
cd viralrecall/
chmod +x viralrecall.py
dos2unix viralrecall.py
wget -O hmm.tar.gz https://zenodo.org/record/4762520/files/hmm.tar.gz?download=1
tar -xvzf hmm.tar.gz
rm hmm.tar.gz

# Need to add custom script to allow ViralRecall to run from any directory (Code from https://github.com/faylward/viralrecall/issues/10)
# Also need to symlink out.txt and err.txt to stdout and stderr to prevent viralrecall.py from creating these in ${CONDA_PREFIX}/share (which it can't because it's root protected)
# Copy contents into viralrecall
chmod +x viralrecall
ln -s /dev/stdout out.txt
ln -s /dev/stderr err.txt
cd ../../bin/
ln -s ../share/viralrecall/viralrecall

python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif viralrecall -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



