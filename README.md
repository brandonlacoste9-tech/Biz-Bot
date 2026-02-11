# Biz-Bot

A multi-tenant WhatsApp/web automation platform for SMBs that captures leads, books appointments, answers FAQs, and runs bilingual (FR-CA/EN) workflows—with enterprise AI, monitoring, and secure, production-ready deployment.

## 🚀 Features

- **Multi-Tenant Architecture**: Support multiple businesses with isolated data
- **WhatsApp Integration**: Automated conversations via Twilio
- **Voice AI**: Natural language voice interactions with ElevenLabs
- **Bilingual Support**: English and French Canadian (FR-CA)
- **Appointment Booking**: Automated scheduling system
- **Lead Capture**: Intelligent lead qualification and tracking
- **AI-Powered**: GPT-4 integration for natural conversations
- **Production Ready**: Docker orchestration with monitoring and logging
- **Secure**: TLS/SSL, secrets management, and security headers

## 📋 Prerequisites

- **Docker** (v20.10 or higher)
- **Docker Compose** (v2.0 or higher)
- **Node.js** (v18 or higher) - for local development
- **PostgreSQL** (v15) - included in Docker setup
- **Redis** (v7) - included in Docker setup

## 🛠️ Quick Start

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git
   cd Biz-Bot
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` with your credentials**
   ```bash
   nano .env  # or your preferred editor
   ```

4. **Start development environment**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   - Application: http://localhost:3000
   - Health Check: http://localhost:3000/health
   - Metrics: http://localhost:3000/metrics

### Production Deployment

#### On Your VPS (155.138.139.53)

1. **SSH into your VPS**
   ```bash
   ssh root@155.138.139.53
   ```

2. **Clone the repository**
   ```bash
   cd /opt
   git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git
   cd Biz-Bot
   ```

3. **Setup secrets**
   ```bash
   ./scripts/setup-secrets.sh
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env
   ```
   Update these critical values:
   - `VPS_IP=155.138.139.53`
   - `DOMAIN=yourdomain.com`
   - `SSL_EMAIL=admin@yourdomain.com`
   - `NODE_ENV=production`

5. **Setup SSL certificates**
   ```bash
   ./scripts/setup-ssl.sh
   ```

6. **Deploy the stack**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

7. **Verify deployment**
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   docker-compose -f docker-compose.prod.yml logs -f app
   ```

## 🏗️ Architecture

### Services

- **app**: Node.js Express application
- **nginx**: Reverse proxy with TLS termination
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **prometheus**: Metrics collection
- **grafana**: Metrics visualization
- **node-exporter**: System metrics

### Network Architecture

```
Internet → Nginx (443) → App (3000)
                       ↓
                 PostgreSQL (5432)
                       ↓
                   Redis (6379)
                       ↓
                 Prometheus (9090) → Grafana (3001)
```

## 📊 Monitoring

### Prometheus
Access Prometheus at `http://your-vps-ip:9090`
- Metrics collection every 15 seconds
- Custom application metrics
- System metrics via node-exporter

### Grafana
Access Grafana at `http://your-vps-ip:3001`
- Default credentials: admin/admin (change on first login)
- Pre-configured Biz-Bot dashboard
- Real-time monitoring and alerting

### Metrics Endpoints
- Application metrics: `https://yourdomain.com/metrics`
- Health check: `https://yourdomain.com/health`

## 🔒 Security

### Secrets Management
All sensitive credentials are stored as Docker secrets:
- Never committed to git
- Encrypted at rest
- Mounted read-only in containers

### SSL/TLS
- Let's Encrypt certificates (free, auto-renewing)
- TLS 1.2/1.3 only
- Modern cipher suites
- HSTS enabled

### Security Headers
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy
- Content-Security-Policy (nginx)

### Rate Limiting
- API endpoints: 10 requests/second
- General endpoints: 100 requests/second
- Configurable per route

## 🔧 Configuration

### Environment Variables

Key configuration in `.env`:

```bash
# Application
NODE_ENV=production
PORT=3000
APP_URL=https://yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/bizbot

# API Keys
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
ELEVENLABS_API_KEY=your_key
OPENAI_API_KEY=your_key

# Security
JWT_SECRET=your_secret
ENCRYPTION_KEY=your_key
```

See `.env.example` for complete configuration options.

## 🧪 Testing

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run linter
npm run lint
```

## 📝 API Documentation

### Health Check
```bash
GET /health
Response: {
  "status": "healthy",
  "timestamp": "2024-02-11T17:00:00.000Z",
  "uptime": 3600
}
```

### API Status
```bash
GET /api/status
Response: {
  "api": "v1",
  "status": "operational",
  "features": {
    "whatsapp": "enabled",
    "voice": "enabled",
    "multiTenant": "enabled"
  }
}
```

### Webhooks
```bash
POST /webhooks/twilio
Content-Type: application/json
# Twilio webhook payload
```

## 🚢 Deployment Commands

```bash
# Start development
docker-compose up -d

# Start production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Deploy via script
./scripts/deploy.sh
```

## 🔄 Maintenance

### Database Backups
```bash
# Backup
docker exec biz-bot-postgres pg_dump -U bizbot bizbot > backup.sql

# Restore
docker exec -i biz-bot-postgres psql -U bizbot bizbot < backup.sql
```

### Log Rotation
Logs are automatically rotated by Docker. Configure in docker-compose:
```yaml
logging:
  options:
    max-size: "10m"
    max-file: "3"
```

### Certificate Renewal
SSL certificates auto-renew via cron (runs twice daily):
```bash
# Manual renewal
certbot renew
docker-compose restart nginx
```

## 🐛 Troubleshooting

### Services won't start
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs

# Check disk space
df -h

# Check memory
free -h
```

### SSL Certificate Issues
```bash
# Verify certificates
certbot certificates

# Test nginx config
docker exec biz-bot-nginx nginx -t

# Regenerate certificates
./scripts/setup-ssl.sh
```

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Connect to database
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot

# Verify credentials in .env
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Twilio API](https://www.twilio.com/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [ElevenLabs API](https://docs.elevenlabs.io/)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

For support, email support@yourdomain.com or open an issue in the repository.

## 🎯 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Multi-language support (beyond EN/FR-CA)
- [ ] Analytics dashboard
- [ ] Mobile app integration
- [ ] Advanced AI conversation flows
- [ ] CRM integrations
- [ ] Payment processing

---

**Built with ❤️ for SMBs**
