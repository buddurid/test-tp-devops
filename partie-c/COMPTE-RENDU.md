# Compte rendu - Partie C : Pipeline CI/CD GitHub Actions

## Déclenchement

Le workflow [ci.yml](../.github/workflows/ci.yml) se déclenche à chaque push
sur `main` et à chaque pull request destinée à `main`. Aucun serveur Jenkins
ou webhook supplémentaire n'est nécessaire : GitHub Actions utilise des
runners GitHub.

## Étapes

Pour chaque push ou pull request, le pipeline :

1. récupère le code ;
2. installe Python 3.12 ;
3. installe les dépendances de développement ;
4. exécute les tests unitaires de `partie-b/tests`.

Après un push réussi sur `main`, le second job :

1. construit l'image Docker ;
2. se connecte à Docker Hub ;
3. publie les tags `latest` et le SHA du commit.

## Configuration GitHub

Dans le dépôt GitHub, ouvrir **Settings → Secrets and variables → Actions** et
créer les secrets :

- `DOCKERHUB_USERNAME` : votre nom d'utilisateur Docker Hub ;
- `DOCKERHUB_TOKEN` : un access token Docker Hub, et non votre mot de passe.

L'image publiée sera :

```text
DOCKERHUB_USERNAME/counter-app:latest
DOCKERHUB_USERNAME/counter-app:<SHA_DU_COMMIT>
```

Les secrets ne sont pas enregistrés dans le dépôt.

## Vérification locale

```bash
PYTHONPATH=partie-b pytest -q partie-b/tests
docker build -t counter-app:ci partie-b
```

## Consulter le résultat

Dans GitHub, ouvrir l'onglet **Actions**, sélectionner **CI/CD Visit-Counter**,
puis ouvrir l'exécution du commit concerné pour consulter les logs des jobs
`Tests unitaires` et `Build et publication Docker`.
