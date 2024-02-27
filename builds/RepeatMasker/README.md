# Containerize RepeatMasker

## v4.1.6 (Dfam3.8 - Partition 0)

### Revision 1

```
program="RepeatMasker"
version="4.1.6"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda ${program}=4.1.5
conda activate ${conda_env}
$mamba install -y -p ${conda_env} -c bioconda bedtools=2.31.1

# Copy aux seq renaming scrips to conda bin/
cp rename_sequences.py   ${conda_env}/bin/rename_sequences
cp unrename_sequences.py ${conda_env}/bin/unrename_sequences

# Replace existing RepeatMasker v4.1.5 with v4.1.6 (since its not yet available on conda)
cd ${conda_env}/share/
rm -r RepeatMasker

wget https://www.repeatmasker.org/RepeatMasker/RepeatMasker-4.1.6.tar.gz
tar -zxvf RepeatMasker-4.1.6.tar.gz
rm RepeatMasker-4.1.6.tar.gz

##
## Download Dfam3.8 data (just partiation 0)
##
# Partition 0 [dfam38_full.0.h5]: root - Mammalia, Amoebozoa, Bacteria <bacteria>, Choanoflagellata, Rhodophyta, Haptista, Metamonada, Fungi, Sar, Placozoa, Ctenophora <comb jellies>, Filasterea, Spiralia, Discoba, Cnidaria, Porifera, Viruses
#     Consensi: 295552, HMMs: 295552
#
# Partition 1 [dfam38_full.1.h5]: Obtectomera 
#     Consensi: 611842, HMMs: 611842
#
# Partition 2 [dfam38_full.2.h5]: Euteleosteomorpha 
#     Consensi: 517633, HMMs: 517633
#
# Partition 3 [dfam38_full.3.h5]: Sarcopterygii - Sauropsida, Coelacanthimorpha, Amphibia, Dipnomorpha
#     Consensi: 397995, HMMs: 397995
#
# Partition 4 [dfam38_full.4.h5]: Diptera 
#     Consensi: 345905, HMMs: 345905
#
# Partition 5 [dfam38_full.5.h5]: Viridiplantae 
#     Consensi: 176667, HMMs: 176667
#
# Partition 6 [dfam38_full.6.h5]: Deuterostomia - Chondrichthyes, Hemichordata, Cladistia, Holostei, Tunicata, Cephalochordata, Cyclostomata <vertebrates>, Osteoglossocephala, Otomorpha, Elopocephalai, Echinodermata, Chondrostei
#     Consensi: 280588, HMMs: 280588
#
# Partition 7 [dfam38_full.7.h5]: Hymenoptera 
#     Consensi: 321661, HMMs: 321661
#
# Partition 8 [dfam38_full.8.h5]: Ecdysozoa - Nematoda, Gelechioidea, Yponomeutoidea, Incurvarioidea, Chelicerata, Collembola, Polyneoptera, Tineoidea, Apoditrysia, Monocondylia, Strepsiptera, Palaeoptera, Neuropterida, Crustacea, Coleoptera, Siphonaptera, Trichoptera, Paraneoptera, Myriapoda, Scalidophora
#     Consensi: 626235, HMMs: 626235
#
cd ${conda_env}/share/RepeatMasker/Libraries/famdb/
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.0.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.0.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.1.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.1.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.2.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.2.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.3.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.3.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.4.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.4.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.5.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.5.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.6.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.6.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.7.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.7.h5.gz.md5sum
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.8.h5.gz
wget https://www.dfam.org/releases/Dfam_3.8/families/FamDB/dfam38_full.8.h5.gz.md5sum

# NOTE: Download all partitions but only use 0 with RepeatMasker since they are too large to include then all (>700GB total).

# Unpack all files.
md5sum -c *.md5sum
gunzip *.h5.gz

# Get fasta formated partitions (NOTE: need to have partition 0 with lower partitions for famdb to work)
mkdir fasta; cd fasta/
for i in {1..8}; do ( mkdir dfam38_full.$i.h5; cd dfam38_full.$i.h5; ln -s ../../dfam38_full.0.h5; ln -s ../../dfam38_full.$i.h5 ); done
for i in {0..8}; do echo "python ${conda_env}/share/RepeatMasker/famdb.py -i dfam38_full.$i.h5 families --format fasta_name -ad root > dfam38_full.$i.fa"; done | parallel -j 10

# Copy everything over to conda
# Need to do this depending on where you downloaded everything

# Rebuild RepeatMasker library
PATH="${conda_env}/bin:$PATH"
./configure

conda env config vars set PERL5LIB=${conda_env}/share/RepeatMasker
# May have to manually edit:
# $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh


python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif RepeatMasker -help
singularity exec ${prefix}.sif rename_sequences
singularity exec ${prefix}.sif unrename_sequences
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



