# Containerize RStudio

## RStudio with R v3.6.3

### Revision 1

```
prefix="rstudio_r3.6.3-rev1"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



## RStudio with R v4.0.4

### Revision 1

```
prefix="rstudio_r4.0.4-rev1"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



## RStudio with R v4.1.2-

### Revision 1

```
prefix="rstudio_r4.1.2-rev1"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



## RStudio with R v4.2.3

### Revision 1

```
prefix="rstudio_r4.2.3-rev1"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```



## RStudio with R v4.3.2

### Revision 1

```
prefix="rstudio_r4.3.2-rev1"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/





prefix="rstudio_r4.3.2-rev2"

singularity build --fakeroot --force ${prefix}.sif ${prefix}.def

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```

