# Containerize MetaBAT

## v2.17-21-g2740d8d

### Revision 1

```
program="MetaBAT"
version="2.17-21-g2740d8d"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build ${prefix}.sif ${prefix}.def

singularity exec ${prefix}.sif metabat2 --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



