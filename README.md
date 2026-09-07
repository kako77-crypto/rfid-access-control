# RFID Access Control

Monorepo de la plateforme de contrôle d'accès RFID. Cette première phase fournit
l'infrastructure minimale : API FastAPI, interface React et base MariaDB. Les
fonctionnalités métier et le firmware ne font pas encore partie de cette version.

## Prérequis

- Docker avec le plugin Compose
- Pour le développement local : Python 3.12+ et Node.js 22+

## Démarrage avec Docker

```bash
cp .env.example .env
docker compose up --build
```

Une fois les healthchecks au vert :

- frontend : http://localhost:5173
- API : http://localhost:8000
- documentation OpenAPI : http://localhost:8000/docs
- santé API : http://localhost:8000/health
- disponibilité API et MariaDB : http://localhost:8000/ready

MariaDB n'est volontairement publiée sur aucun port de l'hôte. Arrêter la pile
avec `docker compose down`, ou supprimer aussi ses données avec
`docker compose down -v`.

## Développement et qualité

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
ruff check .
pytest
```

Les migrations Alembic sont préparées dans `backend/migrations`. Aucune migration
métier n'est créée durant cette phase.

### Frontend

```bash
cd frontend
npm install
npm run lint
npm test
npm run build
```

## Organisation

```text
backend/   API FastAPI, configuration SQLAlchemy/Alembic et tests
frontend/  application React + TypeScript + Vite et tests
compose.yaml  orchestration et healthchecks des trois services
```

Les secrets réels doivent uniquement être placés dans `.env`, ignoré par Git.
Les valeurs de `.env.example` sont fictives et doivent être remplacées hors du
dépôt pour tout environnement partagé ou de production.
