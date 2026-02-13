# 🚀 PetHelper Bot - Release Plan

## Overview

This document outlines the complete deployment and release process for the PetHelper Veterinary Bot.

## Table of Contents

1. [Pre-Release Checklist](#pre-release-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Deployment Options](#deployment-options)
5. [Post-Release Tasks](#post-release-tasks)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Rollback Plan](#rollback-plan)

---

## Pre-Release Checklist

### Code Review
- [ ] All handlers tested locally
- [ ] Database migrations reviewed
- [ ] Security audit completed
- [ ] Environment variables documented
- [ ] No hardcoded secrets in code
- [ ] Logging configured properly
- [ ] Error handling implemented

### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual testing completed
- [ ] Load testing performed
- [ ] Database connection tested
- [ ] Redis connection tested (if using)

### Documentation
- [ ] README.md updated
- [ ] API documentation complete
- [ ] Deployment guide reviewed
- [ ] Environment variables documented
- [ ] Architecture diagram created

### Security
- [ ] Sensitive data encrypted
- [ ] API tokens secured
- [ ] Database credentials secured
- [ ] HTTPS configured (for webhooks)
- [ ] Rate limiting configured
- [ ] Input validation implemented

---

## Environment Setup

### 1. Server Requirements

#### Minimum Requirements
- **OS**: Ubuntu 20.04 LTS or newer
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum
- **Storage**: 20GB SSD
- **Network**: Stable internet connection

#### Software Requirements
- Docker 24.0+
- Docker Compose 2.0+
- Git
- Make (optional, for automation)

### 2. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Verify installations
docker --version
docker compose version

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Clone Repository

```bash
# Clone your repository
git clone https://github.com/yourusername/my_vet_bot.git
cd my_vet_bot

# Checkout production branch
git checkout production  # or main
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here

# Database Configuration
POSTGRES_DB=vetbot
POSTGRES_USER=vetbot_user
POSTGRES_PASSWORD=strong_password_here
POSTGRES_PORT=5432

# Redis Configuration (optional)
REDIS_PORT=6379

# Application Settings
DEBUG=False
LOG_LEVEL=INFO

# Monitoring (optional)
ENABLE_SENTRY=False
SENTRY_DSN=your_sentry_dsn_here
```

---

## Database Setup

### 1. Initialize Database

```bash
# Start only PostgreSQL first
docker compose up -d postgres

# Wait for PostgreSQL to be ready
docker compose logs -f postgres

# Run migrations (if using Alembic)
docker compose run --rm bot alembic upgrade head
```

### 2. Seed Initial Data (Optional)

```bash
# Run seed script
docker compose run --rm bot python scripts/seed_data.py
```

### 3. Backup Strategy

```bash
# Create backup directory
mkdir -p backups

# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker compose exec -T postgres pg_dump -U vetbot_user vetbot > backups/backup_$DATE.sql
echo "Backup created: backups/backup_$DATE.sql"
EOF

chmod +x backup.sh

# Add to crontab for daily backups
crontab -e
# Add: 0 2 * * * /path/to/my_vet_bot/backup.sh
```

---

## Deployment Options

### Option 1: Docker Compose (Recommended for VPS)

#### Start All Services

```bash
# Build and start all services
docker compose up -d --build

# Check logs
docker compose logs -f

# Check status
docker compose ps
```

#### Update Deployment

```bash
# Pull latest changes
git pull origin production

# Rebuild and restart
docker compose up -d --build

# Remove old images
docker image prune -f
```

### Option 2: Manual Deployment (Without Docker)

#### Install Python Dependencies

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Setup PostgreSQL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE vetbot;
CREATE USER vetbot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE vetbot TO vetbot_user;
\q
```

#### Run Bot

```bash
# With systemd service
sudo nano /etc/systemd/system/vetbot.service
```

```ini
[Unit]
Description=PetHelper Veterinary Bot
After=network.target postgresql.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/my_vet_bot
Environment="PATH=/path/to/my_vet_bot/venv/bin"
ExecStart=/path/to/my_vet_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable vetbot
sudo systemctl start vetbot
sudo systemctl status vetbot
```

### Option 3: Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-vetbot-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set BOT_TOKEN=your_token_here

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

#### Railway/Render

1. Connect GitHub repository
2. Add PostgreSQL database addon
3. Set environment variables
4. Deploy automatically on push

---

## Post-Release Tasks

### 1. Verify Deployment

```bash
# Check all services are running
docker compose ps

# Check bot logs
docker compose logs bot

# Test bot functionality
# Send /start command in Telegram
```

### 2. Configure Monitoring

#### Setup Sentry (Error Tracking)

```bash
# Sign up at sentry.io
# Get DSN and add to .env
ENABLE_SENTRY=True
SENTRY_DSN=https://your-dsn@sentry.io/project-id

# Restart bot
docker compose restart bot
```

#### Setup Logging

```bash
# Create log rotation
sudo nano /etc/logrotate.d/vetbot
```

```
/path/to/my_vet_bot/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    missingok
    copytruncate
}
```

### 3. Performance Optimization

#### Enable Redis Caching

```bash
# Redis is already in docker-compose.yml
# Ensure REDIS_URL is set in .env
REDIS_URL=redis://redis:6379

# Restart services
docker compose restart bot
```

#### Database Optimization

```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_pets_owner_id ON pets(owner_id);
CREATE INDEX idx_reminders_user_id ON reminders(user_id);
CREATE INDEX idx_ads_created_at ON ads(created_at DESC);
```

### 4. Setup Webhooks (Optional, for Production)

```bash
# Setup Nginx reverse proxy
sudo apt install nginx certbot python3-certbot-nginx

# Configure SSL
sudo certbot --nginx -d your-domain.com

# Configure Nginx
sudo nano /etc/nginx/sites-available/vetbot
```

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location /webhook {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/vetbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Update .env for webhook mode
WEBHOOK_ENABLED=True
WEBHOOK_URL=https://your-domain.com
```

---

## Monitoring & Maintenance

### 1. Daily Checks

```bash
# Check bot status
docker compose ps

# Check recent logs
docker compose logs --tail=50 bot

# Check database size
docker compose exec postgres psql -U vetbot_user -d vetbot -c "SELECT pg_size_pretty(pg_database_size('vetbot'));"

# Check disk space
df -h
```

### 2. Weekly Maintenance

```bash
# Database backup
./backup.sh

# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean Docker resources
docker system prune -f

# Review error logs
grep ERROR logs/bot.log | tail -20
```

### 3. Monthly Tasks

- Review and analyze user statistics
- Update dependencies (check for security updates)
- Database optimization (VACUUM, ANALYZE)
- Review and update documentation
- Test backup restoration

### 4. Monitoring Dashboard

Consider setting up:
- **Grafana + Prometheus** for metrics
- **ELK Stack** for log analysis
- **Uptime monitoring** (UptimeRobot, Pingdom)

---

## Rollback Plan

### Quick Rollback

```bash
# Stop current deployment
docker compose down

# Checkout previous version
git log --oneline  # Find previous commit
git checkout <previous-commit-hash>

# Restore database backup (if needed)
docker compose up -d postgres
cat backups/backup_YYYYMMDD_HHMMSS.sql | docker compose exec -T postgres psql -U vetbot_user vetbot

# Restart services
docker compose up -d --build

# Verify
docker compose logs -f bot
```

### Database Rollback

```bash
# Rollback migrations (if using Alembic)
docker compose run --rm bot alembic downgrade -1

# Or restore from backup
cat backups/backup_latest.sql | docker compose exec -T postgres psql -U vetbot_user vetbot
```

---

## Troubleshooting

### Bot Not Starting

```bash
# Check logs
docker compose logs bot

# Check environment variables
docker compose exec bot env | grep BOT_TOKEN

# Test database connection
docker compose exec bot python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker compose ps postgres

# Check connection from bot
docker compose exec bot pg_isready -h postgres -U vetbot_user

# Review connection string
echo $DATABASE_URL
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check bot memory usage
docker compose exec bot ps aux

# Analyze slow queries
docker compose exec postgres psql -U vetbot_user -d vetbot -c "SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"
```

---

## Support & Updates

### Getting Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
docker compose pull

# Rebuild and restart
docker compose up -d --build
```

### Reporting Issues

- Check logs first
- Document steps to reproduce
- Include relevant log excerpts
- Note bot version and environment

---

## Checklist Summary

### Pre-Launch
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database initialized
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Documentation complete

### Launch Day
- [ ] Deploy to production
- [ ] Verify all services running
- [ ] Test core functionality
- [ ] Monitor logs for errors
- [ ] Announce to users

### Post-Launch
- [ ] Daily monitoring for first week
- [ ] Collect user feedback
- [ ] Fix critical bugs immediately
- [ ] Plan next iteration

---

## Contacts & Resources

- **Bot Owner**: [Your contact]
- **Technical Support**: [Support email]
- **Documentation**: [Wiki/Docs URL]
- **Repository**: [GitHub URL]
- **Status Page**: [Status monitoring URL]

---

**Last Updated**: 2024-02-13
**Version**: 2.0.0
