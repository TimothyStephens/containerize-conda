

```bash
program=maxbin2
version=2.2.7
tgs_version=5
tag="${program,,}:${version}-TGSv${tgs_version}"

docker build -t timothystephens/${tag} .
docker run timothystephens/${tag} run_MaxBin.pl -h
docker push timothystephens/${tag}

singularity pull ${tag}.sif docker://timothystephens/${tag}
singularity exec ${tag}.sif run_MaxBin.pl -h
rm ${tag}.sif

docker image ls
docker image rm XXXX
```



