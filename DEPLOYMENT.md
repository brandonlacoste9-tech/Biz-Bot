# Biz-Bot Production Deployment Guide

Complete guide for deploying Biz-Bot to production on VPS at 155.138.139.53

## 📋 Pre-Deployment Checklist

### 1. VPS Requirements
- [ ] Ubuntu 20.04+ or Debian 11+
- [ ] Minimum 2 CPU cores
- [ ] Minimum 4GB RAM
- [ ] Minimum 40GB storage
- [ ] Root or sudo access
- [ ] Public IP: 155.138.139.53

### 2. Domain Setup
- [ ] Domain registered and pointing to 155.138.139.53
- [ ] DNS A record configured
- [ ] DNS propagation complete (check with `dig yourdomain.com`)

### 3. Required Credentials
- [ ] Twilio Account SID
- [ ] Twilio Auth Token
- [ ] Twilio Phone Number
- [ ] ElevenLabs API Key
- [ ] OpenAI API Key
- [ ] Email for SSL certificate notifications

## 🚀 Step-by-Step Deployment

### Step 1: Initial VPS Setup

```bash
# SSH into your VPS
ssh root@155.138.139.53

# Update system packages
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Verify installations
docker --version
docker compose version

# Install additional tools
apt install -y git curl wget nginx certbot
```

### Step 2: Clone Repository

```bash
# Create application directory
mkdir -p /opt/biz-bot
cd /opt/biz-bot

# Clone repository
git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git .

# Set proper permissions
chmod +x scripts/*.sh
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
```

**Critical settings to update:**

```bash
# Application
NODE_ENV=production
PORT=3000
APP_NAME=Biz-Bot
APP_URL=https://yourdomain.com

# VPS Configuration
VPS_IP=155.138.139.53
DOMAIN=yourdomain.com
SSL_EMAIL=admin@yourdomain.com

# Database (generate strong passwords)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASSWORD=$(openssl rand -base64 16)

# Rate Limiting (adjust based on your needs)
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

### Step 4: Setup Secrets

```bash
# Run interactive secrets setup
./scripts/setup-secrets.sh
```

This will prompt you to enter:
1. Twilio Account SID
2. Twilio Auth Token
3. ElevenLabs API Key
4. OpenAI API Key
5. JWT Secret (auto-generated if empty)
6. Encryption Key (auto-generated if empty)
7. PostgreSQL Password

**Alternatively, create secrets manually:**

```bash
# Create secrets directory
mkdir -p secrets

# Create secret files
echo "your_twilio_sid" > secrets/twilio_account_sid.txt
echo "your_twilio_token" > secrets/twilio_auth_token.txt
echo "your_elevenlabs_key" > secrets/elevenlabs_api_key.txt
echo "your_openai_key" > secrets/openai_api_key.txt
echo "$(openssl rand -base64 32)" > secrets/jwt_secret.txt
echo "$(openssl rand -base64 32)" > secrets/encryption_key.txt
echo "$(openssl rand -base64 32)" > secrets/postgres_password.txt

# Secure permissions
chmod 600 secrets/*.txt
```

### Step 5: Setup SSL Certificates

```bash
# Update domain in script or set environment variable
export DOMAIN=yourdomain.com
export SSL_EMAIL=admin@yourdomain.com

# Run SSL setup script
./scripts/setup-ssl.sh
```

**Manual SSL setup (if script fails):**

```bash
# Stop nginx if running
docker-compose down nginx

# Create webroot directory
mkdir -p /var/www/certbot

# Obtain certificate
certbot certonly --standalone \
    -d yourdomain.com \
    --email admin@yourdomain.com \
    --agree-tos \
    --non-interactive

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
chmod 644 nginx/ssl/fullchain.pem
chmod 600 nginx/ssl/privkey.pem
```

### Step 6: Configure Firewall

```bash
# Install ufw if not present
apt install ufw -y

# Configure firewall rules
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 9090/tcp  # Prometheus (optional, can restrict to specific IPs)
ufw allow 3001/tcp  # Grafana (optional, can restrict to specific IPs)

# Enable firewall
ufw --force enable

# Check status
ufw status
```

### Step 7: Deploy the Stack

```bash
# Build Docker images
docker compose -f docker-compose.prod.yml build

# Start all services
docker compose -f docker-compose.prod.yml up -d

# Verify all services are running
docker compose -f docker-compose.prod.yml ps

# Check logs
docker compose -f docker-compose.prod.yml logs -f
```

### Step 8: Verify Deployment

```bash
# Test health endpoint
curl http://localhost:3000/health

# Test HTTPS (replace with your domain)
curl https://yourdomain.com/health

# Check service status
docker compose -f docker-compose.prod.yml ps

# View application logs
docker compose -f docker-compose.prod.yml logs app

# View nginx logs
docker compose -f docker-compose.prod.yml logs nginx
```

### Step 9: Access Monitoring

1. **Prometheus**: http://155.138.139.53:9090
   - Check targets: http://155.138.139.53:9090/targets
   - View metrics and create queries

2. **Grafana**: http://155.138.139.53:3001
   - Login: admin / [password from .env]
   - View Biz-Bot dashboard
   - Configure additional dashboards

### Step 10: Setup Monitoring Alerts (Optional)

Configure Prometheus Alertmanager for email/Slack notifications:

```bash
# Create alertmanager configuration
cat > monitoring/prometheus/alertmanager.yml << 'ALERT'
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@yourdomain.com'
  smtp_auth_username: 'your_email@gmail.com'
  smtp_auth_password: 'your_app_password'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'email'

receivers:
  - name: 'email'
    email_configs:
      - to: 'admin@yourdomain.com'
ALERT

# Add alertmanager to docker-compose.prod.yml
# Then restart services
docker compose -f docker-compose.prod.yml restart
```

## 🔄 Post-Deployment Tasks

### 1. Setup Automated Backups

```bash
# Create backup script
cat > /opt/biz-bot/scripts/backup.sh << 'BACKUP'
#!/bin/bash
BACKUP_DIR="/opt/backups/biz-bot"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker exec biz-bot-postgres pg_dump -U bizbot bizbot | \
    gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup secrets (encrypted)
tar czf $BACKUP_DIR/secrets_$DATE.tar.gz secrets/

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
BACKUP

chmod +x /opt/biz-bot/scripts/backup.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /opt/biz-bot/scripts/backup.sh >> /var/log/biz-bot-backup.log 2>&1" | crontab -
```

### 2. Setup Log Rotation

```bash
# Create logrotate configuration
cat > /etc/logrotate.d/biz-bot << 'LOGROTATE'
/opt/biz-bot/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        docker compose -f /opt/biz-bot/docker-compose.prod.yml restart app
    endscript
}
LOGROTATE
```

### 3. Configure Twilio Webhooks

In your Twilio console:
1. Navigate to Phone Numbers → Manage → Active Numbers
2. Click your WhatsApp-enabled number
3. Set webhook URL: `https://yourdomain.com/webhooks/twilio`
4. Set HTTP method: POST
5. Save configuration

### 4. Test End-to-End

```bash
# Send test WhatsApp message to your Twilio number
# Check logs for webhook receipt
docker compose logs -f app | grep webhook

# Verify database entry
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot \
    -c "SELECT * FROM conversations ORDER BY created_at DESC LIMIT 5;"
```

## 🔍 Monitoring & Maintenance

### Daily Checks

```bash
# Check service health
docker compose -f docker-compose.prod.yml ps

# Check disk usage
df -h

# Check memory
free -h

# View recent errors
docker compose logs --tail=100 app | grep -i error
```

### Weekly Tasks

- Review Grafana dashboards
- Check Prometheus alerts
- Review application logs
- Verify backups completed
- Update SSL certificate status

### Monthly Tasks

- Security updates: `apt update && apt upgrade -y`
- Review and rotate secrets if needed
- Analyze metrics and optimize resources
- Review and clean up old logs/backups

## 🚨 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs [service-name]

# Check disk space
df -h

# Check memory
free -h

# Restart specific service
docker compose restart [service-name]
```

### SSL Certificate Issues

```bash
# Check certificate status
certbot certificates

# Force renewal
certbot renew --force-renewal

# Copy new certificates
cp /etc/letsencrypt/live/yourdomain.com/*.pem nginx/ssl/
docker compose restart nginx
```

### Database Connection Issues

```bash
# Check postgres logs
docker compose logs postgres

# Connect to database
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot

# Check connections
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot \
    -c "SELECT * FROM pg_stat_activity;"
```

### High Memory Usage

```bash
# Check container stats
docker stats

# Restart containers
docker compose restart

# Adjust memory limits in docker-compose.prod.yml
```

## 📊 Performance Optimization

### 1. Database Optimization

```sql
-- Connect to database
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot

-- Analyze tables
ANALYZE;

-- Vacuum database
VACUUM;

-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 2. Redis Configuration

```bash
# Monitor Redis
docker exec -it biz-bot-redis redis-cli INFO

# Check memory usage
docker exec -it biz-bot-redis redis-cli INFO memory

# Monitor commands
docker exec -it biz-bot-redis redis-cli MONITOR
```

### 3. Nginx Tuning

Adjust in `nginx/nginx.conf`:
```nginx
worker_processes auto;
worker_connections 2048;
keepalive_timeout 30;
```

## 🔄 Updates & Upgrades

### Application Updates

```bash
cd /opt/biz-bot

# Pull latest changes
git pull origin main

# Rebuild and restart
docker compose -f docker-compose.prod.yml up -d --build

# Verify
docker compose ps
docker compose logs -f app
```

### System Updates

```bash
# Update packages
apt update && apt upgrade -y

# Update Docker
apt install docker-ce docker-ce-cli containerd.io -y

# Restart services
docker compose restart
```

## 📞 Support & Resources

- **Documentation**: See README.md
- **Issues**: GitHub Issues
- **Logs**: `/var/log/` and `docker compose logs`
- **Monitoring**: Grafana dashboards

## ✅ Deployment Verification Checklist

- [ ] All services running (`docker compose ps`)
- [ ] Health endpoint responding (`curl https://yourdomain.com/health`)
- [ ] HTTPS working with valid certificate
- [ ] Prometheus collecting metrics
- [ ] Grafana accessible and showing data
- [ ] Database initialized with tables
- [ ] Redis cache operational
- [ ] Twilio webhooks configured
- [ ] Backups configured and tested
- [ ] Firewall rules applied
- [ ] Monitoring alerts configured
- [ ] Log rotation configured
- [ ] Documentation reviewed

---

**Congratulations! Your Biz-Bot production deployment is complete! 🎉**
