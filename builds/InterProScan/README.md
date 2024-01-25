# Containerize InterProScan

## v5.65-97.0

### Revision 1

```
program="InterProScan"
version="5.65-97.0"
revision="1"
prefix="${program}_v${version}-rev${revision}"
conda_env="/opt/conda/envs/${prefix}"
mamba=$(which mamba)

$mamba create -y -p ${conda_env} -c bioconda perl=5.32.1 python=3.12.0 openjdk=11.0.15
conda activate ${conda_env}
cd ${conda_env}/share/

mkdir my_interproscan
cd my_interproscan
wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.65-97.0/interproscan-5.65-97.0-64-bit.tar.gz
wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.65-97.0/interproscan-5.65-97.0-64-bit.tar.gz.md5
md5sum -c interproscan-5.65-97.0-64-bit.tar.gz.md5
tar -pxvzf interproscan-5.65-97.0-*-bit.tar.gz

# Download Phobius through browser
http://phobius.sbc.su.se/data.html

tar -zxvf phobius101_linux.tgz
cp phobius/decodeanhmm.64bit my_interproscan/interproscan-5.65-97.0/bin/phobius/1.01/decodeanhmm
cp phobius/phobius.model my_interproscan/interproscan-5.65-97.0/bin/phobius/1.01/
cp phobius/phobius.options my_interproscan/interproscan-5.65-97.0/bin/phobius/1.01/
cp phobius/phobius.pl my_interproscan/interproscan-5.65-97.0/bin/phobius/1.01/

# Add to interproscan.properties
phobius.signature.library.release=1.01
binary.phobius.pl.path=bin/phobius/1.01/phobius.pl


# Download SignalP v4.1 through browser
https://services.healthtech.dtu.dk/cgi-bin/sw_request?software=signalp&version=4.1&packageversion=4.1g&platform=Linux

tar -zxvf signalp-4.1g.Linux.tar.gz
mv signalp-4.1/* my_interproscan/interproscan-5.65-97.0/bin/signalp/4.1/

# Add to interproscan.properties
signalp_euk.signature.library.release=4.1
signalp_gram_positive.signature.library.release=4.1
signalp_gram_negative.signature.library.release=4.1
binary.signalp.path=bin/signalp/4.1/signalp
signalp.perl.library.dir=bin/signalp/4.1/lib

# confirm that the following line in the “signalp” binary is set to the required location:
BEGIN {
    $ENV{SIGNALP} = 'bin/signalp/4.1';
}


# Download TMHMM v2.0c through browser
https://services.healthtech.dtu.dk/cgi-bin/sw_request?software=tmhmm&version=2.0c&packageversion=2.0c&platform=Linux

tar -zxvf tmhmm-2.0c.Linux.tar.gz
cp tmhmm-2.0c/bin/decodeanhmm.Linux_x86_64 my_interproscan/interproscan-5.65-97.0/bin/tmhmm/2.0c/decodeanhmm
cp tmhmm-2.0c/bin/tmhmm my_interpiroscan/interproscan-5.65-97.0/bin/tmhmm/2.0c/
cp tmhmm-2.0c/bin/tmhmmformat.pl my_interproscan/interproscan-5.65-97.0/bin/tmhmm/2.0c/

cp tmhmm-2.0c/lib/TMHMM2.0.model my_interproscan/interproscan-5.65-97.0/data/tmhmm/2.0c/TMHMM2.0c.model
cp tmhmm-2.0c/lib/TMHMM2.0.options my_interproscan/interproscan-5.65-97.0/data/tmhmm/2.0c/TMHMM2.0c.options

# Add to interproscan.properties
tmhmm.signature.library.release=2.0c
binary.tmhmm.path=bin/tmhmm/2.0c/decodeanhmm
tmhmm.model.path=data/tmhmm/2.0c/TMHMM2.0c.model


# Add interproscan.sh symlink
cd ${conda_env}/bin
ln -s ../share/my_interproscan/interproscan-5.65-97.0/interproscan.sh


python ../../conda_to_singularity.py --template ${prefix}.def ${conda_env} ${prefix}.sif

rm -fr ${conda_env}
singularity exec ${prefix}.sif interproscan.sh --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



