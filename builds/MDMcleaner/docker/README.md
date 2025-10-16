

```bash
program=mdmcleaner
version=0.8.7

docker build -t timothystephens/${program,,}:${version}-TGS .
docker run timothystephens/${program,,}:${version}-TGS mdmcleaner -h
docker push timothystephens/${program,,}:${version}-TGS

singularity pull ${program,,}_${version}-TGS.sif docker://timothystephens/${program,,}:${version}-TGS
singularity exec ${program,,}_${version}-TGS.sif mdmcleaner -h
rm ${program,,}_${version}-TGS.sif

docker image ls
docker image rm XXXX
```



