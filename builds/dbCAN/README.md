# Containerize dbCAN

## 4.1.4

### Revision 1

```
program="dbCAN"
version="4.1.1"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

singularity exec ${prefix}.sif run_dbcan -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



