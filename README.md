# TP DevOps - Conteneurisation, orchestration et pipeline

Les livrables sont séparés par partie :

- [Partie B](./partie-b/) : application Flask Visit-Counter, Dockerfile,
  Compose, tests et [compte rendu Markdown](./partie-b/COMPTE-RENDU.md) ;
- [Partie C](./partie-c/) : pipeline GitHub Actions et
  [compte rendu Markdown](./partie-c/COMPTE-RENDU.md).

## Démarrage rapide de la partie B

```bash
cd partie-b
cp .env.example .env
docker compose up -d
curl http://localhost:8080/
```

Les identifiants Docker Hub et les secrets GitHub Actions ne sont pas inclus dans le
dépôt. Ils doivent être configurés localement avant la publication.
