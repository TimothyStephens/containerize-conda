# Containerize ESMFold

## v2.0.1

### Revision 1

```bash
program="ESMFold"
version="2.0.1"
cuda_version="11.8.0"
revision="1"
prefix="${program}_v${version}_cuda_v${cuda_version}-rev${revision}"

cat ${prefix}.def \
  | sed -e "s/{{COLABFOLD_VERSION}}/$version/g" -e "s/{{CUDA_VERSION}}/$cuda_version/g" -e "s/{{REVISION}}/$revision/g" \
  | singularity build --fakeroot --force ${prefix}.sif /dev/stdin 

singularity exec ${prefix}.sif esm-fold -h
singularity run-help ${prefix}.sif

chown root ${prefix}.sif
mv ${prefix}.sif /scratch/singularity/
```


