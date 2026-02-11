# Biz-Bot

Biz-Bot: A multi-tenant WhatsApp/web automation platform for Quebec SMBs that captures leads, books appointments, answers FAQs, and runs bilingual (FR-CA/EN) workflows—with enterprise AI, monitoring, and secure, production-ready deployment.

## Features

- 🏢 **Multi-tenant Architecture**: Isolated data and settings per business
- 🔐 **Magic Link Authentication**: Passwordless email authentication
- 📱 **WhatsApp & SMS Integration**: Via Twilio for customer communication
- 🎙️ **Voice Integration**: ElevenLabs for voice interactions
- 📅 **Smart Booking System**: Appointment management with status tracking
- ❓ **FAQ Management**: Bilingual FAQ system with search
- 🌍 **Internationalization**: Full FR-CA/EN support
- 👨‍💼 **Admin Dashboard**: Platform management and statistics
- 🔒 **Tenant Isolation**: Secure data separation between tenants
- 🏥 **Health Endpoints**: Ready for production monitoring

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management
- **SQLAlchemy**: ORM for database operations
- **Twilio**: SMS/WhatsApp integration
- **ElevenLabs**: Voice AI integration

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **next-intl**: Internationalization (FR-CA/EN)
- **Axios**: API client

### Infrastructure
- **Docker Compose**: Development environment
- **PostgreSQL 15**: Database container
- **Redis 7**: Cache container

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker Compose

1. **Clone the repository**
   ```bash
   git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git
   cd Biz-Bot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (Twilio, ElevenLabs)
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database with seed data**
   ```bash
   docker-compose exec backend python -m app.utils.seed_data
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup (without Docker)

#### Backend Setup

1. **Create a virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL and Redis**
   - Install PostgreSQL 15
   - Install Redis 7
   - Update DATABASE_URL and REDIS_URL in .env

4. **Run database migrations and seed data**
   ```bash
   python -m app.utils.seed_data
   ```

5. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

3. **Access the frontend**
   - Open http://localhost:3000

## Testing

### Backend Tests

```bash
cd backend
pytest app/tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Project Structure

```
Biz-Bot/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configurations
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── utils/        # Utilities & seed data
│   │   ├── tests/        # Tests
│   │   └── main.py       # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js app directory
│   │   ├── components/   # React components
│   │   ├── lib/          # API client & utilities
│   │   └── types/        # TypeScript types
│   ├── messages/         # i18n translations
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## API Endpoints

### Health
- `GET /api/health/` - Basic health check
- `GET /api/health/ready` - Readiness check (includes DB)
- `GET /api/health/live` - Liveness check

### Authentication
- `POST /api/auth/magic-link/request` - Request magic link
- `POST /api/auth/magic-link/verify` - Verify magic link
- `GET /api/auth/me` - Get current user

### Tenants
- `POST /api/tenants/` - Create tenant
- `GET /api/tenants/{id}` - Get tenant
- `PATCH /api/tenants/{id}` - Update tenant
- `GET /api/tenants/` - List tenants (admin)

### Bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/` - List bookings
- `GET /api/bookings/{id}` - Get booking
- `PATCH /api/bookings/{id}` - Update booking
- `DELETE /api/bookings/{id}` - Delete booking

### FAQ
- `POST /api/faq/` - Create FAQ item
- `GET /api/faq/` - List FAQ items
- `GET /api/faq/search` - Search FAQ
- `GET /api/faq/{id}` - Get FAQ item
- `PATCH /api/faq/{id}` - Update FAQ item
- `DELETE /api/faq/{id}` - Delete FAQ item

### Admin
- `GET /api/admin/stats` - Platform statistics
- `GET /api/admin/users` - List all users
- `GET /api/admin/tenants` - List all tenants

### Webhooks
- `POST /api/webhooks/twilio/sms` - Twilio SMS webhook
- `POST /api/webhooks/twilio/whatsapp` - Twilio WhatsApp webhook

## Seed Data

The application includes seed data for development:

### Tenants
1. **Café Le Québécois** (cafe-le-quebecois)
   - Email: contact@cafe-quebecois.ca
   - Users:
     - admin@cafe-quebecois.ca (Admin)
     - manager@cafe-quebecois.ca (Manager)

2. **Clinique Santé Plus** (clinique-sante-plus)
   - Email: info@sante-plus.ca
   - Users:
     - admin@sante-plus.ca (Admin)
     - receptionist@sante-plus.ca (Receptionist)

To login, request a magic link for any of the emails above.

## Configuration

### Environment Variables

See `.env.example` for all available configuration options:

- **Database**: `DATABASE_URL`
- **Redis**: `REDIS_URL`
- **Security**: `SECRET_KEY`, `MAGIC_LINK_SECRET`
- **Twilio**: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, etc.
- **ElevenLabs**: `ELEVENLABS_API_KEY`
- **Frontend**: `NEXT_PUBLIC_API_URL`

## Production Deployment

### Security Checklist
- [ ] Change all default secrets in `.env`
- [ ] Use strong SECRET_KEY and MAGIC_LINK_SECRET
- [ ] Configure CORS properly
- [ ] Use HTTPS for all endpoints
- [ ] Set up proper firewall rules
- [ ] Enable database backups
- [ ] Configure proper logging
- [ ] Set up monitoring and alerts

### Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## Development

### Adding New Features

1. **Backend**: Add endpoints in `backend/app/api/`
2. **Frontend**: Add pages in `frontend/src/app/[locale]/`
3. **Models**: Update database models in `backend/app/models/`
4. **Schemas**: Update Pydantic schemas in `backend/app/schemas/`
5. **Translations**: Update `frontend/messages/en.json` and `fr.json`

### Code Style

- Backend: Follow PEP 8
- Frontend: Use ESLint and Prettier
- Commit messages: Use conventional commits

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres
```

### Frontend Build Issues
```bash
# Clear Next.js cache
cd frontend
rm -rf .next
npm run build
```

### Backend Import Errors
```bash
# Ensure you're in the backend directory and venv is activated
cd backend
source venv/bin/activate
python -m app.main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/brandonlacoste9-tech/Biz-Bot/issues

## Roadmap

- [ ] Enhanced WhatsApp flows
- [ ] Voice call handling
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Advanced AI features
- [ ] Payment integration
- [ ] Multi-channel support
