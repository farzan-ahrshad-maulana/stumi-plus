# OPERATIONS.md

## Stumi Research v1 Operations Guide

Panduan operasional harian untuk menjalankan, memonitor, memperbarui, backup, dan melakukan troubleshooting aplikasi Stumi Research.

---

# Server Information

Application:

```text
Stumi Research v1
```

Production URL:

```text
https://stumi.cloud
```

Project Directory:

```text
/home/stumi/stumi
```

Virtual Environment:

```text
/home/stumi/stumi/.venv
```

Systemd Service:

```text
stumi.service
```

Database:

```text
PostgreSQL
Database: stumi
User: stumi
```

---

# Daily Health Check

Check API:

```bash
curl https://stumi.cloud/health
```

Expected:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

# Check Service Status

```bash
sudo systemctl status stumi
```

Expected:

```text
active (running)
```

---

# View Application Logs

Last 50 lines:

```bash
sudo journalctl -u stumi -n 50 --no-pager
```

Live logs:

```bash
sudo journalctl -u stumi -f
```

---

# Restart Application

```bash
sudo systemctl restart stumi
```

Verify:

```bash
sudo systemctl status stumi
```

---

# Stop Application

```bash
sudo systemctl stop stumi
```

---

# Start Application

```bash
sudo systemctl start stumi
```

---

# Deployment Workflow

## 1. Local Development

Develop and test locally:

```bash
uvicorn app.main:app --reload
```

Commit changes:

```bash
git add .

git commit -m "Your message"

git push
```

---

## 2. Production Deployment

Login VPS:

```bash
ssh stumi@stumi.cloud
```

Go to project:

```bash
cd ~/stumi
```

Pull latest code:

```bash
git pull
```

Activate environment:

```bash
source .venv/bin/activate
```

Install new dependencies if required:

```bash
pip install -r requirements.txt
```

Restart application:

```bash
sudo systemctl restart stumi
```

Verify:

```bash
curl https://stumi.cloud/health
```

---

# Database Operations

Connect database:

```bash
sudo -u postgres psql stumi
```

---

## Count Journals

```sql
SELECT COUNT(*) FROM journals;
```

---

## Count Chunks

```sql
SELECT COUNT(*) FROM chunks;
```

---

## View Recent Journals

```sql
SELECT
    id,
    title,
    publication_year,
    created_at
FROM journals
ORDER BY id DESC
LIMIT 10;
```

---

## Check Embeddings

```sql
SELECT
    id,
    title,
    abstract_embedding IS NOT NULL AS has_embedding
FROM journals;
```

---

# Backup Operations

Backup location:

```text
/home/stumi/backups
```

---

## Manual Backup

```bash
~/backup_stumi.sh
```

Verify:

```bash
ls -lh ~/backups
```

---

## Automated Backup

Check cron:

```bash
crontab -l
```

Expected:

```cron
0 2 * * * /home/stumi/backup_stumi.sh
```

---

# Restore Procedure

Create restore database:

```bash
sudo -u postgres createdb stumi_restore_test
```

Restore:

```bash
pg_restore \
-d stumi_restore_test \
~/backups/FILENAME.backup
```

Verify:

```bash
sudo -u postgres psql stumi_restore_test
```

```sql
\dt
```

Expected:

```text
journals
chunks
```

Remove test database:

```bash
sudo -u postgres dropdb stumi_restore_test
```

---

# Disk Usage

Check disk:

```bash
df -h
```

Check project size:

```bash
du -sh ~/stumi
```

Check backup size:

```bash
du -sh ~/backups
```

---

# Memory Usage

```bash
free -h
```

Expected:

```text
RAM
Swap
```

Both visible.

---

# CPU Monitoring

```bash
htop
```

Install if missing:

```bash
sudo apt install htop
```

---

# Nginx Operations

Check status:

```bash
sudo systemctl status nginx
```

Restart:

```bash
sudo systemctl restart nginx
```

Reload config:

```bash
sudo systemctl reload nginx
```

Test config:

```bash
sudo nginx -t
```

---

# SSL Operations

Check certificate:

```bash
sudo certbot certificates
```

Manual renewal test:

```bash
sudo certbot renew --dry-run
```

---

# Production Smoke Test

## Health

```bash
curl https://stumi.cloud/health
```

---

## Search

```bash
curl -X POST https://stumi.cloud/journals/search \
-H "Content-Type: application/json" \
-d '{
  "query": "machine translation",
  "limit": 10
}'
```

---

## Chat

```bash
curl -X POST https://stumi.cloud/chat/ \
-H "Content-Type: application/json" \
-d '{
  "journal_id": 1,
  "question": "What is Transformer?"
}'
```

---

# Common Problems

## Service Not Running

Check:

```bash
sudo systemctl status stumi
```

Logs:

```bash
sudo journalctl -u stumi -n 100 --no-pager
```

Restart:

```bash
sudo systemctl restart stumi
```

---

## Database Connection Error

Check PostgreSQL:

```bash
sudo systemctl status postgresql
```

Restart:

```bash
sudo systemctl restart postgresql
```

---

## Nginx 502 Bad Gateway

Cause:

```text
FastAPI service stopped
```

Check:

```bash
sudo systemctl status stumi
```

---

## SSL Error

Check:

```bash
sudo certbot certificates
```

Renew:

```bash
sudo certbot renew
```

---

## High Memory Usage

Check:

```bash
free -h
```

Check:

```bash
htop
```

Restart service if necessary:

```bash
sudo systemctl restart stumi
```

---

# Emergency Recovery Checklist

1. Verify VPS reachable.
2. Verify nginx running.
3. Verify PostgreSQL running.
4. Verify stumi service running.
5. Verify health endpoint.
6. Restore latest backup if required.
7. Test search endpoint.
8. Test chat endpoint.

---

# Production Ready Checklist

Infrastructure:

* [ ] VPS online
* [ ] PostgreSQL online
* [ ] Nginx online
* [ ] SSL valid

Application:

* [ ] Health endpoint healthy
* [ ] Search working
* [ ] Chat working

Operations:

* [ ] Backup generated
* [ ] Restore tested
* [ ] Logs accessible

Status:

```text
STUMI PRODUCTION OPERATIONAL
```
