# Containerize BRAKER

## v3.0.6

### Revision 1

```
program="BRAKER"
version="3.0.6"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build ${prefix}.sif ${prefix}.def

singularity exec ${prefix}.sif braker.pl --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



