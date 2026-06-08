# DEPLOYMENT.md

## Stumi Research v1 Deployment Guide

Panduan deployment backend Stumi Research ke VPS Ubuntu.

---

# Server Specification

Production Environment:

* Ubuntu 26.04
* 1 vCPU
* 1 GB RAM
* 60 GB SSD

Domain:

* stumi.cloud
* [www.stumi.cloud](http://www.stumi.cloud)

---

# 1. Install System Packages

Update server:

```bash
sudo apt update
sudo apt upgrade -y
```

Install dependencies:

```bash
sudo apt install -y \
git \
curl \
nginx \
python3 \
python3-pip \
python3-venv
```

---

# 2. Install PostgreSQL

Install PostgreSQL 18:

```bash
sudo apt install postgresql postgresql-contrib -y
```

Verify:

```bash
sudo systemctl status postgresql
```

---

# 3. Create Database

Login PostgreSQL:

```bash
sudo -u postgres psql
```

Create user:

```sql
CREATE USER stumi WITH PASSWORD 'YOUR_PASSWORD';
```

Create database:

```sql
CREATE DATABASE stumi;
```

Grant privileges:

```sql
GRANT ALL PRIVILEGES ON DATABASE stumi TO stumi;
```

Connect database:

```sql
\c stumi
```

Grant schema privileges:

```sql
GRANT ALL ON SCHEMA public TO stumi;

GRANT CREATE ON SCHEMA public TO stumi;

ALTER SCHEMA public OWNER TO stumi;
```

Exit:

```sql
\q
```

---

# 4. Install pgvector

Install extension package:

```bash
sudo apt install postgresql-18-pgvector
```

Activate extension:

```bash
sudo -u postgres psql stumi
```

```sql
CREATE EXTENSION vector;
```

Verify:

```sql
SELECT extname FROM pg_extension;
```

Expected:

```text
plpgsql
vector
```

Exit:

```sql
\q
```

---

# 5. Clone Repository

Create working directory:

```bash
mkdir ~/stumi
cd ~/stumi
```

Clone repository:

```bash
git clone <repository-url> .
```

---

# 6. Create Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

# 7. Configure Environment Variables

Create:

```bash
nano .env
```

Example:

```env
DATABASE_URL=postgresql://stumi:PASSWORD@localhost/stumi

OPENROUTER_API_KEY=YOUR_KEY
```

---

# 8. Create Database Schema

From project root:

```bash
source .venv/bin/activate

python -m app.db.init_db
```

Expected output:

```text
Database initialized
```

Verify:

```bash
sudo -u postgres psql stumi
```

```sql
\dt
```

Expected:

```text
journals
chunks
```

Verify vector columns:

```sql
\d journals
\d chunks
```

Expected:

```text
abstract_embedding vector(1024)
embedding vector(1024)
```

---

# 9. Test Application

Run manually:

```bash
uvicorn app.main:app \
--host 0.0.0.0 \
--port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

# 10. Create Systemd Service

Create:

```bash
sudo nano /etc/systemd/system/stumi.service
```

Content:

```ini
[Unit]
Description=Stumi FastAPI Service
After=network.target

[Service]
User=stumi
Group=stumi

WorkingDirectory=/home/stumi/stumi

Environment="PATH=/home/stumi/stumi/.venv/bin"

ExecStart=/home/stumi/stumi/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload

sudo systemctl enable stumi

sudo systemctl start stumi
```

Verify:

```bash
sudo systemctl status stumi
```

---

# 11. Configure Nginx

Create:

```bash
sudo nano /etc/nginx/sites-available/stumi
```

Content:

```nginx
server {
    server_name stumi.cloud www.stumi.cloud;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable:

```bash
sudo ln -s \
/etc/nginx/sites-available/stumi \
/etc/nginx/sites-enabled/
```

Test:

```bash
sudo nginx -t
```

Reload:

```bash
sudo systemctl reload nginx
```

---

# 12. Configure SSL

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
```

Generate certificate:

```bash
sudo certbot --nginx \
-d stumi.cloud \
-d www.stumi.cloud
```

Verify:

```bash
curl https://stumi.cloud/health
```

---

# 13. Security Hardening

Disable OpenAPI:

```python
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
```

Verify:

```text
/docs
/redoc
/openapi.json
```

Return:

```json
{
  "detail": "Not Found"
}
```

---

# 14. Rate Limiting

Install:

```bash
pip install slowapi
```

Protect expensive endpoints:

```python
@limiter.limit("20/minute")
```

Example:

```python
@router.post("/")
@limiter.limit("20/minute")
def chat(...):
```

---

# 15. Backup

Create:

```bash
nano ~/backup_stumi.sh
```

Content:

```bash
#!/bin/bash

BACKUP_DIR="/home/stumi/backups"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

pg_dump \
-U stumi \
-d stumi \
-F c \
-f "$BACKUP_DIR/stumi_$TIMESTAMP.backup"

find "$BACKUP_DIR" \
-type f \
-name "*.backup" \
-mtime +7 \
-delete
```

Permission:

```bash
chmod +x ~/backup_stumi.sh
```

Test:

```bash
~/backup_stumi.sh
```

---

# 16. Automated Daily Backup

Edit crontab:

```bash
crontab -e
```

Add:

```cron
0 2 * * * /home/stumi/backup_stumi.sh
```

Daily backup at:

```text
02:00 AM
```

---

# 17. Swap Configuration

Create 2GB swap:

```bash
sudo fallocate -l 2G /swapfile

sudo chmod 600 /swapfile

sudo mkswap /swapfile

sudo swapon /swapfile
```

Persist:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Verify:

```bash
free -h
```

---

# 18. Production Validation Checklist

Infrastructure:

* [ ] PostgreSQL installed
* [ ] pgvector installed
* [ ] vector extension enabled
* [ ] schema created
* [ ] SSL active
* [ ] nginx active
* [ ] systemd active

Application:

* [ ] Health endpoint works
* [ ] Journal ingestion works
* [ ] Semantic search works
* [ ] RAG chat works
* [ ] Rate limiting works

Operations:

* [ ] Backup works
* [ ] Restore tested
* [ ] Swap enabled

Deployment Status:

PRODUCTION READY

```
```
