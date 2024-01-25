# Containerize Prokka

## v1.14.6

### Revision 1

```
program="Prokka"
version="1.14.6"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build ${prefix}.sif ${prefix}.def

singularity exec ${prefix}.sif prokka --help
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



