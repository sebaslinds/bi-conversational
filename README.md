# bi-conversational

Backend FastAPI d'un assistant BI conversationnel. Cette API charge un jeu de données de ventes depuis `data/sales.csv`, calcule des indicateurs agrégés, puis répond à des questions métier en français via l'API OpenAI.

## Fonctionnalités

- Chargement et agrégation des données avec `pandas`
- Endpoint `GET /data` pour exposer les KPI et les synthèses
- Endpoint `POST /chat` pour poser des questions métier en langage naturel
- Réponses générées en français avec :
  - 1 insight clé
  - 1 tendance
  - 1 recommandation business concrète
- CORS activé pour l'intégration avec le frontend

## Stack technique

- Python
- FastAPI
- Uvicorn
- Pandas
- python-dotenv
- SDK OpenAI

## Structure du projet

```text
bi-conversational/
+-- data/
¦   +-- sales.csv
+-- .env
+-- .gitignore
+-- main.py
+-- requirements.txt
```

## Prérequis

- Python 3.10 ou plus
- Une clé API OpenAI

## Installation

```bash
pip install -r requirements.txt
```

## Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=votre_cle_api_openai
```

## Lancer le serveur en local

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API disponible sur `http://localhost:8000`.

## Endpoints

### `GET /data`

Retourne les indicateurs calculés à partir du fichier `data/sales.csv`.

Exemple de réponse :

```json
{
  "total_revenue": 43000,
  "total_orders": 145,
  "avg_basket": 296.55,
  "revenue_by_month": {
    "2025-01": 12000,
    "2025-02": 15000
  },
  "revenue_by_category": {
    "Electronique": 21000
  },
  "revenue_by_region": {
    "Quebec": 18000
  }
}
```

### `POST /chat`

Envoie une question métier et retourne une réponse concise générée à partir du résumé courant des ventes.

Corps de requête :

```json
{
  "message": "Quel mois a le plus de revenus ?"
}
```

Exemple de réponse :

```json
{
  "response": "?? Insight...\n?? Tendance...\n?? Recommandation..."
}
```

## Intégration frontend

Ce backend est prévu pour fonctionner avec le dépôt compagnon `bi-frontend`.

Le frontend appelle :

- `GET http://localhost:8000/data`
- `POST http://localhost:8000/chat`

## Notes

- Si `OPENAI_API_KEY` est absent, `POST /chat` retourne une erreur `500`.
- Les données sont relues depuis `data/sales.csv` à chaque appel.
- La configuration CORS actuelle autorise toutes les origines pour faciliter le développement local.
