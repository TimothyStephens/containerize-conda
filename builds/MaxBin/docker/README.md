

```bash
program=maxbin2
version=2.2.7

docker build -t timothystephens/${program,,}:${version}-TGS .
docker run timothystephens/${program,,}:${version}-TGS run_MaxBin.pl -h
docker push timothystephens/${program,,}:${version}-TGS

singularity pull ${program,,}_${version}-TGS.sif docker://timothystephens/${program,,}:${version}-TGS
singularity exec ${program,,}_${version}-TGS.sif run_MaxBin.pl -h
rm ${program,,}_${version}-TGS.sif

docker image ls
docker image rm XXXX
```



