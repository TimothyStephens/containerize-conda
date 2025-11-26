


```bash
program="EggNOG-mapper"
version="2.1.13"
revision="1"

docker build -t timothystephens/${program,,}:${version}-TGSv${revision} .
docker run timothystephens/${program,,}:${version}-TGSv${revision} emapper.py -h
docker push timothystephens/${program,,}:${version}-TGSv${revision}

singularity pull ${program,,}_${version}-TGSv${revision}.sif docker://timothystephens/${program,,}:${version}-TGSv${revision}
singularity exec ${program,,}_${version}-TGSv${revision}.sif emapper.py -h
rm ${program,,}_${version}-TGSv${revision}.sif

docker image ls
docker image rm XXXX
```



