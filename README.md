# mir-test

Applicazione Python containerizzata con Docker, con CI/CD su GitHub Actions e deploy automatico su Google Kubernetes Engine (GKE). Utilizza un database PostgreSQL gestito su Google Cloud SQL.

---

## 🚀 Pipeline CI/CD

Ogni push sul branch `main`:

1. Builda e testa l’applicazione con `pytest`
2. Pusha l’immagine Docker su Artifact Registry
3. Aggiorna il deployment su GKE

---

## 🛠️ Requisiti

- **Python >= 3.12**
- **Docker**
- **Google Cloud SDK (`gcloud`)**
- Cluster GKE configurato
- Artifact Registry creato
- Variabili segrete configurate su GitHub:
  - `GCP_SA_KEY` → JSON della service account
  - `DATABASE_URL` → stringa connessione PostgreSQL
  - `DATABASE_URL_TEST` → stringa connessione PostgreSQL di test
  - `GKE_CLUSTER_NAME` → nome del cluster GKE
  - `GKE_CLUSTER_ZONE` → zona (es. `europe-west3-a`) - OPTIONAL NOT DONE

---

## 🧰 Installazione e Run Locale (+TEST)

### Setup ambiente Python

```bash
python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

### Test 

export DATABASE_URL_TEST=postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DBNAME> (This should be not the prod db url)

pytest app/tests/

## 📦 Build & Push

### Locale

Per buildare e pushare l’immagine Docker manualmente:

```bash
docker build -t europe-west3-docker.pkg.dev/testproject-464712/mir-test-repo/mir-test:latest .
gcloud auth configure-docker europe-west3-docker.pkg.dev
docker push europe-west3-docker.pkg.dev/testproject-464712/mir-test-repo/mir-test:latest

## DB Notes:
The database should not be exposed to the whole internet but limited IPs (if any) and in prod you should use VPCs to protect it.
You can access the db via the GCP console or via DataGrip / DBeaver / pgAdmin ... 