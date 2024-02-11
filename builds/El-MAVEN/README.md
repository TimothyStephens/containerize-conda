# Containerize El-MAVEN

## ret20240130 ( > v0.12.1-beta)

### Revision 1

```
program="El-MAVEN"
version="ret20240130"
revision="1"
prefix="${program}_${version}-rev${revision}"

singularity build --fakeroot --force "${prefix}.sif" "${prefix}.def"

singularity exec ${prefix}.sif peakdetector -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



