

```bash
program=cdhit
version=4.8.1

docker build -t timothystephens/${program,,}:${version} .
docker run timothystephens/${program,,}:${version} cd-hit -h
docker push timothystephens/${program,,}:${version}

singularity pull ${program,,}_${version}.sif docker://timothystephens/${program,,}:${version}
singularity exec ${program,,}_${version}.sif mdmcleaner -h
rm ${program,,}_${version}.sif

docker image ls
docker image rm XXXX
```



