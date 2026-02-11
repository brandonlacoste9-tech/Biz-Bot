# Biz-Bot

**Biz-Bot**: A multi-tenant WhatsApp/web automation platform for Quebec SMBs that captures leads, books appointments, answers FAQs, and runs bilingual (FR-CA/EN) workflows—with enterprise AI, monitoring, and secure, production-ready deployment.

## Features

- 🏢 **Multi-Tenant Architecture** - Isolated data and workflows per business
- 💬 **WhatsApp & SMS Integration** - Twilio-powered messaging
- 🎙️ **Voice AI** - ElevenLabs text-to-speech integration
- 📅 **Booking Management** - Automated appointment scheduling
- ❓ **FAQ Automation** - Smart question answering in English and French
- 🌍 **Bilingual Support** - Full FR-CA and EN localization
- 🔐 **Magic Link Authentication** - Passwordless email login
- 🎯 **Tenant Isolation** - Secure data separation
- 📊 **Admin Dashboard** - Manage tenants and users
- 🏥 **Health Monitoring** - System health endpoints

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **Redis** - Caching layer
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Twilio** - SMS/WhatsApp integration
- **ElevenLabs** - Voice AI

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS
- **next-intl** - Internationalization (i18n)

### DevOps
- **Docker Compose** - Container orchestration for development
- **pytest** - Python testing
- **Jest** - JavaScript testing

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git
cd Biz-Bot
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your API keys (optional for development)
```

### 3. Start services with Docker Compose

```bash
docker-compose up --build
```

This will start:
- **PostgreSQL** on port 5432
- **Redis** on port 6379
- **FastAPI Backend** on port 8000
- **Next.js Frontend** on port 3000

### 4. Run database migrations

```bash
# In a new terminal
docker-compose exec backend alembic upgrade head
```

### 5. Seed demo data

```bash
docker-compose exec backend python seed_data.py
```

### 6. Access the application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Demo Accounts

After seeding data, you can login with:
- `admin@cafe-quebecois.ca` (Café Québécois tenant)
- `admin@techsolutions.ca` (Tech Solutions MTL tenant)

Use the magic link authentication - check the backend console for the login link.

## Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed data
python seed_data.py

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Project Structure

```
Biz-Bot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/          # API endpoints
│   │   ├── core/            # Configuration and security
│   │   ├── db/              # Database session
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # External service integrations
│   ├── alembic/             # Database migrations
│   ├── tests/               # Backend tests
│   ├── requirements.txt
│   └── seed_data.py
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js App Router
│   │   │   ├── auth/       # Authentication pages
│   │   │   ├── dashboard/  # Dashboard pages
│   │   │   └── admin/      # Admin pages
│   │   ├── components/     # React components
│   │   └── lib/            # Utilities
│   ├── public/             # Static assets
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## API Endpoints

### Health
- `GET /health` - Health check
- `GET /` - Root endpoint

### Authentication
- `POST /api/v1/auth/request-magic-link` - Request magic link
- `POST /api/v1/auth/verify-magic-link` - Verify magic link
- `POST /api/v1/auth/register` - Register new user

### Bookings
- `GET /api/v1/bookings` - List bookings
- `POST /api/v1/bookings` - Create booking
- `GET /api/v1/bookings/{id}` - Get booking
- `PUT /api/v1/bookings/{id}` - Update booking
- `DELETE /api/v1/bookings/{id}` - Delete booking

### FAQs
- `GET /api/v1/faqs` - List FAQs
- `POST /api/v1/faqs` - Create FAQ
- `GET /api/v1/faqs/{id}` - Get FAQ
- `PUT /api/v1/faqs/{id}` - Update FAQ
- `DELETE /api/v1/faqs/{id}` - Delete FAQ

### Tenants (Admin)
- `GET /api/v1/tenants` - List tenants
- `POST /api/v1/tenants` - Create tenant
- `GET /api/v1/tenants/{id}` - Get tenant

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `MAGIC_LINK_SECRET` - Magic link token secret
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_WHATSAPP_NUMBER` - Twilio WhatsApp number
- `ELEVENLABS_API_KEY` - ElevenLabs API key
- `FRONTEND_URL` - Frontend URL for magic links

#### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Testing

### Backend Tests

```bash
cd backend
pytest                      # Run all tests
pytest tests/test_main.py  # Run specific test file
pytest --cov               # Run with coverage
```

### Frontend Tests

```bash
cd frontend
npm test                   # Run all tests
npm test -- --watch       # Run in watch mode
```

## Deployment

### Production Checklist

1. ✅ Update `SECRET_KEY` and `MAGIC_LINK_SECRET` with strong random values
2. ✅ Configure proper PostgreSQL and Redis instances
3. ✅ Set up Twilio account and get API credentials
4. ✅ Set up ElevenLabs account and get API key
5. ✅ Configure email service for magic links
6. ✅ Set up SSL/TLS certificates
7. ✅ Configure CORS for production domain
8. ✅ Set up monitoring and logging
9. ✅ Configure backup strategy for database
10. ✅ Review security settings and rate limiting

## Multi-Tenancy

The platform uses tenant isolation at the database level:
- Each tenant has a unique `tenant_id`
- All queries are filtered by tenant
- Users belong to a specific tenant
- API endpoints enforce tenant isolation

## Internationalization (i18n)

The platform supports:
- **English (en)**: Default language
- **French Canadian (fr-ca)**: Quebec French

FAQs can be stored in both languages, and the system will respond based on user preference.

## Integrations

### Twilio (WhatsApp & SMS)
- Configure in `.env` with your Twilio credentials
- WhatsApp sandbox for development
- Production WhatsApp Business API for deployment

### ElevenLabs (Voice AI)
- Text-to-speech for voice responses
- Configurable voice models
- Supports multiple languages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/brandonlacoste9-tech/Biz-Bot/issues
- Documentation: http://localhost:8000/docs (when running locally)

## Roadmap

- [ ] Enhanced booking workflow with reminders
- [ ] Advanced analytics dashboard
- [ ] Custom workflow builder
- [ ] More messaging platform integrations
- [ ] Mobile app
- [ ] Advanced AI-powered responses
- [ ] Payment integration
- [ ] Advanced reporting

---

Built with ❤️ for Quebec SMBs
