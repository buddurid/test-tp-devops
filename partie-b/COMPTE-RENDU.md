# Compte rendu - Partie B : Conteneurisation et orchestration

## 1. Objectif et architecture

L'application `Visit-Counter` est composée de deux services :

- `web` : application Flask servie par Gunicorn ;
- `db` : Redis avec AOF activé pour conserver le compteur dans le volume
  `redis-data`.

Le réseau Docker `app-network` permet à l'application d'appeler Redis avec le
nom DNS `db-service`. Le compteur est incrémenté à chaque requête sur `/`.

## 2. Dockerfile commenté

Voir le [Dockerfile](./Dockerfile).

L'image `python:3.12-slim` est choisie plutôt qu'une image Python complète
pour réduire la taille tout en conservant la compatibilité avec les paquets
Python. Les dépendances sont copiées et installées avant le code : Docker peut
ainsi réutiliser cette couche tant que `requirements.txt` ne change pas.

L'utilisateur `appuser` exécute Gunicorn sans privilèges root. Le serveur
écoute sur le port interne `5000`.

Commandes :

```bash
docker build -t counter-app:1.0 .
docker images counter-app
```

## 3. Réseau, volume et persistance

Déploiement manuel :

```bash
docker network create app-network
docker volume create redis-data
docker run -d --name db-service --network app-network \
  -v redis-data:/data redis:7-alpine redis-server --appendonly yes
docker run -d --name counter-app --network app-network \
  -p 8080:5000 counter-app:1.0
```

Test de persistance :

```bash
docker rm -f db-service
docker run -d --name db-service --network app-network \
  -v redis-data:/data redis:7-alpine redis-server --appendonly yes
```

Le volume n'est pas supprimé avec le conteneur, donc la valeur de `hits` est
conservée. Preuve à capturer :

```bash
docker network inspect app-network
docker volume inspect redis-data
```

> **Capture à insérer :** résultat de `docker network inspect app-network`
> montrant `db-service` et `counter-app`.

## 4. Compose et scaling

Le fichier [docker-compose.yml](./docker-compose.yml) centralise les services,
le réseau, le volume, le healthcheck et la variable `WEB_PORT` du fichier
[.env](./.env).

```bash
docker compose up -d
curl http://localhost:${WEB_PORT:-8080}/
docker compose logs -f
```

Une publication de port hôte est une réservation exclusive. Trois réplicas ne
peuvent donc pas publier simultanément le même port :

```bash
docker compose up -d --scale web=3
```

La solution théorique consiste à ne publier qu'un reverse proxy/load balancer
(Nginx, Traefik ou HAProxy) sur le port hôte. Il distribue les requêtes vers
les trois conteneurs `web` sur le réseau Docker.

## 5. Différence entre `RUN` et `CMD`

`RUN` est exécuté pendant le build et produit une couche dans l'image, par
exemple l'installation des dépendances. `CMD` indique le processus par défaut
lancé au démarrage d'un conteneur ; il peut être remplacé par une commande
passée à `docker run`.

## 6. Captures et publication

> **Capture à insérer :** `docker images counter-app` avec la taille de
> l'image.

> **Capture à insérer :** application ouverte dans le navigateur, montrant le
> nombre de visites et l'identifiant du conteneur.

Publication, après authentification :

```bash
docker login
docker tag counter-app:1.0 DOCKERHUB_USER/counter-app:1.0
docker push DOCKERHUB_USER/counter-app:1.0
```

Lien Docker Hub : `https://hub.docker.com/r/DOCKERHUB_USER/counter-app`

## 7. Nettoyage

```bash
docker compose down --volumes --rmi local
docker rm -f db-service counter-app 2>/dev/null || true
docker network rm app-network 2>/dev/null || true
docker volume rm redis-data 2>/dev/null || true
```
