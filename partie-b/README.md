# Partie B - Visit-Counter

## Lancement manuel

```bash
docker build -t counter-app:1.0 .
docker network create app-network
docker volume create redis-data
docker run -d --name db-service --network app-network \
  -v redis-data:/data redis:7-alpine redis-server --appendonly yes
docker run -d --name counter-app --network app-network -p 8080:5000 counter-app:1.0
```

Après suppression de `db-service`, le volume `redis-data` est conservé :

```bash
docker rm -f db-service
docker run -d --name db-service --network app-network \
  -v redis-data:/data redis:7-alpine redis-server --appendonly yes
```

## Compose

```bash
cp .env.example .env
docker compose up -d
curl http://localhost:8080/
docker compose up -d --scale web=3
```

Avec trois réplicas, Docker ne peut pas publier trois fois le même port hôte
`WEB_PORT`. En pratique, on retire `ports` des réplicas et on place un reverse
proxy/load balancer (Nginx, Traefik ou HAProxy) devant les trois conteneurs.

`RUN` exécute une commande pendant la construction de l'image et crée une
couche persistante dans l'image. `CMD` définit la commande par défaut exécutée
au démarrage d'un conteneur ; elle peut être remplacée par `docker run`.

## Nettoyage

```bash
docker compose down --volumes --rmi local
docker rm -f db-service counter-app 2>/dev/null || true
docker network rm app-network 2>/dev/null || true
docker volume rm redis-data 2>/dev/null || true
```
