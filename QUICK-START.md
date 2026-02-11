# Biz-Bot Quick Start Guide

Get Biz-Bot up and running in minutes!

## 🚀 For Development (Local)

```bash
# 1. Clone the repository
git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git
cd Biz-Bot

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env with your local settings (optional for dev)
nano .env

# 4. Start development environment
make dev
# or: docker-compose up -d

# 5. Verify it's running
curl http://localhost:3000/health

# 6. View logs
make logs
# or: docker-compose logs -f
```

**Access Points:**
- Application: http://localhost:3000
- Health: http://localhost:3000/health
- Metrics: http://localhost:3000/metrics
- PostgreSQL: localhost:5432 (user: bizbot, password: bizbot123)
- Redis: localhost:6379

## 🌐 For Production (VPS)

### Prerequisites
- VPS with Ubuntu 20.04+ (e.g., 155.138.139.53)
- Domain pointing to your VPS
- Root or sudo access

### Step 1: Initial VPS Setup

```bash
# SSH into your VPS
ssh root@155.138.139.53

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Clone repository
mkdir -p /opt/biz-bot
cd /opt/biz-bot
git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git .
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your production values
nano .env
```

**Critical settings to change:**
```bash
NODE_ENV=production
APP_URL=https://yourdomain.com
DOMAIN=yourdomain.com
VPS_IP=155.138.139.53
SSL_EMAIL=admin@yourdomain.com
```

### Step 3: Setup Secrets

```bash
# Run interactive setup
./scripts/setup-secrets.sh

# You'll be prompted for:
# - Twilio Account SID
# - Twilio Auth Token
# - ElevenLabs API Key
# - OpenAI API Key
# - Other credentials (auto-generated if left empty)
```

### Step 4: Configure Firewall

```bash
# Setup UFW firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 9090/tcp  # Prometheus (optional)
ufw allow 3001/tcp  # Grafana (optional)
ufw --force enable
```

### Step 5: Setup SSL Certificates

```bash
# Run SSL setup script
export DOMAIN=yourdomain.com
export SSL_EMAIL=admin@yourdomain.com
./scripts/setup-ssl.sh
```

### Step 6: Deploy

```bash
# Deploy the production stack
make prod
# or: docker-compose -f docker-compose.prod.yml up -d

# Verify services are running
make prod-status
# or: docker-compose -f docker-compose.prod.yml ps

# Check logs
make prod-logs
# or: docker-compose -f docker-compose.prod.yml logs -f
```

### Step 7: Verify

```bash
# Test health endpoint
curl https://yourdomain.com/health

# Should return:
# {"status":"healthy","timestamp":"...","uptime":...}
```

## 📊 Access Your Services

After successful deployment:

- **Application**: https://yourdomain.com
- **API**: https://yourdomain.com/api/status
- **Prometheus**: http://155.138.139.53:9090
- **Grafana**: http://155.138.139.53:3001
  - Default login: admin / admin (change on first login)

## 🔧 Common Commands

### Development
```bash
make dev          # Start development
make logs         # View logs
make down         # Stop services
make restart      # Restart services
make db-shell     # Access database
make redis-shell  # Access Redis
```

### Production
```bash
make prod         # Start production
make prod-logs    # View production logs
make prod-down    # Stop production
make backup       # Backup database
make deploy       # Full deployment
```

### Monitoring
```bash
make health       # Check app health
make metrics      # Open Prometheus
make grafana      # Open Grafana
```

## 🔍 Troubleshooting

### Service won't start
```bash
# Check logs
docker-compose logs [service-name]

# Check disk space
df -h

# Restart specific service
docker-compose restart [service-name]
```

### SSL certificate issues
```bash
# Check certificate status
certbot certificates

# Renew manually
certbot renew
docker-compose restart nginx
```

### Database connection issues
```bash
# Connect to database
make db-shell

# Check database logs
docker-compose logs postgres
```

### Can't access application
```bash
# Check if services are running
docker-compose ps

# Check nginx logs
docker-compose logs nginx

# Check firewall
ufw status

# Verify domain DNS
dig yourdomain.com
```

## 📚 Next Steps

1. **Configure Twilio Webhooks**
   - Go to Twilio Console
   - Set webhook URL: `https://yourdomain.com/webhooks/twilio`

2. **Setup Monitoring Alerts**
   - Configure email/Slack in Prometheus Alertmanager
   - See DEPLOYMENT.md for details

3. **Customize Application**
   - Add your business logic in `src/`
   - Implement conversation flows
   - Add appointment booking logic

4. **Setup Backups**
   - Configure automated backups (see DEPLOYMENT.md)
   - Test backup and restore procedures

5. **Review Security**
   - Change default Grafana password
   - Review firewall rules
   - Rotate secrets regularly

## 🆘 Getting Help

- **Documentation**: See README.md for detailed information
- **Deployment**: See DEPLOYMENT.md for comprehensive guide
- **Contributing**: See CONTRIBUTING.md for development guidelines
- **Summary**: See SUMMARY.md for architecture overview

## ✅ Success Checklist

- [ ] Services are running (`docker-compose ps`)
- [ ] Health endpoint returns 200 (`curl https://yourdomain.com/health`)
- [ ] HTTPS is working with valid certificate
- [ ] Prometheus is collecting metrics
- [ ] Grafana dashboards are showing data
- [ ] Database is accessible
- [ ] Redis is operational
- [ ] Firewall is configured
- [ ] Backups are configured
- [ ] Twilio webhooks are set

---

**That's it! Your Biz-Bot is now running! 🎉**

For more detailed information, see the full documentation in README.md and DEPLOYMENT.md.
