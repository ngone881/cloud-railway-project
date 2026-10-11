# 🛍️ NgoneShop – Cloud Deployment (FastAPI + MongoDB Atlas + Railway)

## 🧾 Project Description

**NgoneShop** is a REST API built with **FastAPI** in Python, enabling the management of an IT product catalog for an online store.

The data is stored in **MongoDB Atlas**, and the application is **deployed on Railway** via Railway's **native GitHub integration**, which automatically redeploys the API on every push to the `main` branch.

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: MongoDB Atlas — base de données MongoDB hébergée et gérée dans le cloud (database `products`)
- **CI/CD**: Déploiement continu via l'intégration GitHub native de Railway
- **PaaS**: Railway (plateforme de déploiement cloud, similaire à Heroku/Render)
- **Deployed URL**: [https://cloud-railway-project-production.up.railway.app](https://cloud-railway-project-production.up.railway.app)

---

## 🗄️ MongoDB Atlas Configuration

1. Create a **free cluster (M0)** at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a **database user** with:
   - Username (`MONGO_USERNAME`)
   - Password (`MONGO_PASSWORD`)
3. Create a database named `products`
4. Inside it, create a collection `products` (optional, will be auto-created)
5. Go to **Network Access** and allow access from all IPs: 0.0.0.0/0, since Railway (on the free plan) doesn't provide a static IP address, so I can't restrict MongoDB Atlas to a specific Railway IP without a paid plan.
6. Copy the connection URI and dynamically replace credentials in your code

---

## 🔐 Environment Variables

### `.env` file (used only locally)

env
APP_LOCAL_PORT=8000
MONGO_USERNAME=<username>
MONGO_PASSWORD=<password>
MONGO_DB_NAME=products

✅ The .env file is ignored from GitHub using .gitignore to protect sensitive information.

---

Environment Variables on Railway

Add the following to Railway > Project > Variables:
- APP_LOCAL_PORT: 8000 (optional, Railway handles PORT)
- MONGO_USERNAME: same as MongoDB Atlas
- MONGO_PASSWORD: same as MongoDB Atlas
- MONGO_DB_NAME: products

---

🚀 Déploiement automatique via Railway

Railway est connecté directement à ce dépôt via son **intégration GitHub native** (l'app GitHub "railway-app"). Railway surveille la branche `main` et redéploie automatiquement l'API à chaque push, sans intervention d'un pipeline GitHub Actions.

Le dépôt contient également un workflow GitHub Actions (décrit ci-dessous) correspondant à une configuration CI/CD alternative, syntaxiquement valide, qui se déclenche bien sur chaque push. ⚠️ Son premier run (#24) a cependant échoué, probablement en raison de l'absence de crédit Railway actif sur le compte. Quoi qu'il en soit, **il ne s'agit pas du mécanisme utilisé pour les déploiements réels** : les déploiements historiques visibles dans l'onglet Deployments de Railway (25 au total) ont tous été effectués via l'intégration Railway-GitHub native décrite ci-dessus, indépendamment de ce workflow. Les étapes suivantes sont conservées à titre de documentation technique.

## 1. Setup on Railway
Create a project at https://railway.app
Connect my GitHub repository
Add the environment variables listed above
Copy my RAILWAY_TOKEN from my Railway account settings


## 2. GitHub Secrets (configuration CI/CD non utilisée pour le déploiement actif)

In GitHub, go to Settings > Secrets and variables > Actions and add:
RAILWAY_TOKEN=<my_railway_token>


## 3. GitHub Actions Workflow (.github/workflows/deploy.yml) — se déclenche sur push, mais non utilisé pour le déploiement réel

    name: Deploy to Railway

    on:
    push:
        branches:
        - main

    jobs:
    deploy:
        runs-on: ubuntu-latest

        steps:
        - name: Checkout code
            uses: actions/checkout@v3

        - name: Set up Python
            uses: actions/setup-python@v4
            with:
            python-version: '3.11'

        - name: Install dependencies
            run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt

        - name: Install Railway CLI
            run: npm install -g @railway/cli

        - name: Deploy to Railway
            env:
            RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
            run: railway up --service cloud-railway-project

## 4. Procfile

web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}


## 5. runtime.txt

python-3.11

## 📂 Project Structure 
    .
    ├── app/
    │   ├── __init__.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   └── routes.py
    ├── .github/
    │   └── workflows/
    │       └── deploy.yml
    ├── .env                # not versioned (local use only)
    ├── .gitignore
    ├── Procfile
    ├── runtime.txt
    ├── requirements.txt
    └── README.md

## 🔐 Security

The .env file with sensitive data is ignored using .gitignore
The Railway token is securely stored in GitHub Actions Secrets


## ✅ Expected Result

Each push to the `main` branch is automatically picked up by **Railway's native GitHub integration**, which rebuilds and redeploys the API to Railway — no GitHub Actions pipeline is involved in this process.

⚠️ Démo live actuellement indisponible (crédit d'essai Railway expiré). Le code reste consultable et fonctionnel en local (voir section Installation).

🔗 Live App: 
https://cloud-railway-project-production.up.railway.app

📄 API Documentation

[https://cloud-railway-project-production.up.railway.app/docs](https://cloud-railway-project-production.up.railway.app/docs) 

[https://cloud-railway-project-production.up.railway.app/redoc](https://cloud-railway-project-production.up.railway.app/redoc)

## 🧪 API Features

The API supports full CRUD operations for products.

**Example: Create a product (POST /api/products/)**

```json
{
  "name": "Logitech K380 Wireless Keyboard",
  "description": "Compact Bluetooth multi-device keyboard",
  "price": 55000,
  "category": "peripherals",
  "quantity": 25,
  "in_stock": true
}
```

Other routes:

- GET /api/products/ – List all products

- GET /api/products/{id} – Get a single product

- PUT /api/products/{id} – Update product

- DELETE /api/products/{id} – Delete product

- ➡️ All routes are testable using the Swagger interface.



