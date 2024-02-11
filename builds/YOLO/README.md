# Containerize YOLO

## v8.1.8-cpu

### Revision 1

```
program="YOLO"
version="8.1.8_cpu"
revision="1"
prefix="${program}_v${version}-rev${revision}"

singularity build ${prefix}.sif ${prefix}.def

singularity exec ${prefix}.sif yolo
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



