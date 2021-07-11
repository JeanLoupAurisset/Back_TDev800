# django
## Comment deployer sur son environnement
### 1) Se logguer sur le repository gitlab d'images docker
Utilisez vos identifiants gitlab pour vous connecter
``` sh
docker login registry.gitlab.com
```
### 2) Pull l'image du projet

``` sh
docker pull registry.gitlab.com/bigshoes/django/djangopg:latest
```

### 3) Lancez l'image docker

``` sh
docker run --name API -p 8000:8000 -d registry.gitlab.com/bigshoes/django/djangopg:latest python3 /BackEnd/manage.py runserver 0.0.0.0:8000 --noreload
```

### 4) Testez l'image
En local lancez une requête vers l'adresse 0.0.0.0:80000

En distanciel mapez le port 8000 à un port disponible de votre serveur ( imaginons ici le port 6952 )
Retrouvez l'adresse ip de votre serveur à l'aide d'ifconfig

Lancez une requête vers l'adresse ${Votre Adresse IP}:${le port choisi}
