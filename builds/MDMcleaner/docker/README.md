

```bash
program=mdmcleaner
version=0.8.7
tgs_version=4

docker build -t timothystephens/${program,,}:${version}-TGSv${tgs_version} .
docker run timothystephens/${program,,}:${version}-TGSv${tgs_version} mdmcleaner -h
docker push timothystephens/${program,,}:${version}-TGSv${tgs_version}

singularity pull ${program,,}_${version}-TGSv${tgs_version}.sif docker://timothystephens/${program,,}:${version}-TGSv${tgs_version}
singularity exec ${program,,}_${version}-TGSv${tgs_version}.sif mdmcleaner -h
rm ${program,,}_${version}-TGSv${tgs_version}.sif

docker image ls
docker image rm XXXX
```



