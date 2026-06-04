

```bash
program=BUSCO
version=6.0.0
tgs_version=1
tag="${program,,}:${version}-TGSv${tgs_version}"

docker build -t timothystephens/${tag} .
docker run timothystephens/${tag} busco -h
docker push timothystephens/${tag}

singularity pull ${tag}.sif docker://timothystephens/${tag}
singularity exec ${tag}.sif busco -h
rm ${tag}.sif

docker image ls
docker image rm XXXX
```



