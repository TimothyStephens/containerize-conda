# Containerize RepeatMasker and RepeatModeler using TETools DockerHub Image

## 1.88

The following software is included in the Dfam TE Tools container (version 1.88):

RepeatModeler	2.0.5	http://www.repeatmasker.org/RepeatModeler/
RepeatMasker	4.1.6	http://www.repeatmasker.org/RMDownload.html
coseg	0.2.3	http://www.repeatmasker.org/COSEGDownload.html
RMBlast	2.14.1	http://www.repeatmasker.org/RMBlast.html
HMMER	3.3.2	http://hmmer.org/
TRF	4.09.1	https://github.com/Benson-Genomics-Lab/TRF
RepeatScout	1.0.6	http://www.repeatmasker.org/RepeatScout-1.0.6.tar.gz
RECON	1.08	http://www.repeatmasker.org/RepeatModeler/RECON-1.08.tar.gz
cd-hit	4.8.1	https://github.com/weizhongli/cdhit
genometools	1.6.4	https://github.com/genometools/genometools
LTR_retriever	2.9.0	https://github.com/oushujun/LTR_retriever/
MAFFT	7.471	https://mafft.cbrc.jp/alignment/software/
NINJA	0.97-cluster_only	https://github.com/TravisWheelerLab/NINJA
UCSC utilities\*	v413	http://hgdownload.soe.ucsc.edu/admin/exe/>
\* Selected tools only: faToTwoBit, twoBitInfo, twoBitToFa

### Revision 1

```
program="RepeatAnalysis"
version="1.88"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build ${prefix}.sif ${prefix}.def

singularity exec ${prefix}.sif RepeatMasker -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



