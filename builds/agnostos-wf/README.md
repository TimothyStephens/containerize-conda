# Containerize agnostos-wf

## v1.1.1

### Revision 1

```
program="agnostos-wf"
version="1.1.1"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

singularity build --fakeroot ${prefix}.sif ${prefix}.def















$mamba env create -p ${conda_env} -f workflow.yml
$mamba install -p ${conda_env} conda-forge::ncurses


## EGGnog-mapper
conda activate ${conda_env}
mkdir -p ${conda_env}/lib/python3.9/site-packages/data
download_eggnog_data.py -P


## OD-seq
cd ${conda_env}/lib
wget http://www.bioinf.ucd.ie/download/od-seq.tar.gz
tar -zxf od-seq.tar.gz
rm od-seq.tar.gz
cd OD-Seq/
g++ -fopenmp -o ${conda_env}/bin/OD-seq AliReader.cpp Bootstrap.cpp DistCalc.cpp DistMatReader.cpp DistWriter.cpp FastaWriter.cpp IQR.cpp ODseq.cpp PairwiseAl.cpp Protein.cpp ResultWriter.cpp runtimeargs.cpp util.cpp


## HMMER MPI
cd ${conda_env}/lib
wget http://eddylab.org/software/hmmer/hmmer-3.3.tar.gz
tar zxf hmmer-3.3.tar.gz
rm hmmer-3.3.tar.gz
cd hmmer-3.3
./configure --prefix="${PWD}" --enable-mpi
make -j 8
make check
make install
cp bin/* ../../bin/


## Parasail
cd ${conda_env}/lib
git clone https://github.com/jeffdaily/parasail
cd parasail
sed -i "s|int matches = parasail_result_get_matches(result);|int matches = parasail_result_get_similar(result);|" apps/parasail_aligner.cpp
autoreconf -fi
./configure --prefix=${conda_env}/lib/parasail
make -j 8
make install

cp ${conda_env}/lib/parasail/bin/* ${conda_env}/bin/

conda env config vars set LD_LIBRARY_PATH=${conda_env}/lib:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
# May have to manually edit:
# $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh


## Igraph C-library
# Built on Amarel since it wont compile on Coral for some unknown reason.
# /usr/bin/gcc --version
# gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44)
# 
# /projects/community/cmake/3.24.3/sw1088/bin/cmake --version
# cmake version 3.24.3
# 
wget https://github.com/igraph/igraph/releases/download/0.10.4/igraph-0.10.4.tar.gz
tar xvfz igraph-0.10.4.tar.gz
rm igraph-0.10.4.tar.gz
cd igraph-0.10.4
mkdir build && cd build

cmake -DCMAKE_INSTALL_PREFIX=${PWD}/bin/igraph ..
cmake --build .
cmake --install .
cd ../../../

export LD_LIBRARY_PATH=${PWD}/bin/igraph/lib64:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

module load cmake/3.24.3-sw1088
gcc is_connected.c -o is_connected -I${PWD}/bin/igraph/include -L${PWD}/bin/igraph/lib64 -ligraph -lm -lstdc++ -lgomp -lpthread
gcc filter_graph.c -o filter_graph -I${PWD}/bin/igraph/include -L${PWD}/bin/igraph/lib64 -ligraph -lm -lstdc++ -lgomp -lpthread

# Copy compiled files to ${conda_env}/bin


python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env} /opt/conda/envs/gcc5
singularity exec ${prefix}.sif grip --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



