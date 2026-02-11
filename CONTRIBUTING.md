# Contributing to Biz-Bot

Thank you for your interest in contributing to Biz-Bot! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Biz-Bot.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/brandonlacoste9-tech/Biz-Bot.git
cd Biz-Bot

# Copy environment file
cp .env.example .env

# Start with Docker Compose
docker-compose up --build

# In another terminal, run migrations
docker-compose exec backend alembic upgrade head

# Seed demo data
docker-compose exec backend python seed_data.py
```

## Project Structure

```
Biz-Bot/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   ├── alembic/     # Database migrations
│   └── tests/       # Backend tests
├── frontend/        # Next.js frontend
│   ├── src/        # Source code
│   └── messages/   # i18n translations
└── docker-compose.yml
```

## Coding Standards

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable names

Example:
```python
def create_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db)
) -> Booking:
    """
    Create a new booking in the database.
    
    Args:
        booking: Booking data to create
        db: Database session
        
    Returns:
        Created booking object
    """
    db_booking = BookingModel(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
```

### Frontend (TypeScript/React)
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful component and variable names

Example:
```typescript
interface BookingCardProps {
  booking: Booking;
  onUpdate: (id: number) => void;
}

export function BookingCard({ booking, onUpdate }: BookingCardProps) {
  return (
    <div className="booking-card">
      <h3>{booking.customer_name}</h3>
      {/* ... */}
    </div>
  );
}
```

## Testing

### Backend Tests
```bash
cd backend
pytest                      # Run all tests
pytest tests/test_main.py  # Run specific test file
pytest --cov              # Run with coverage
```

### Frontend Tests
```bash
cd frontend
npm test                   # Run all tests
npm test -- --watch       # Run in watch mode
```

## Adding New Features

### Backend Endpoint
1. Create a new router in `backend/app/api/v1/`
2. Define schemas in `backend/app/schemas/`
3. Add models if needed in `backend/app/models/`
4. Include router in `backend/app/main.py`
5. Write tests in `backend/tests/`
6. Update API documentation

### Frontend Page
1. Create page in `src/app/`
2. Add translations to `messages/en.json` and `messages/fr-ca.json`
3. Create reusable components in `src/components/`
4. Add API client functions if needed
5. Write tests

## Database Migrations

When changing models:
```bash
# Generate migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Review and edit migration file
# Apply migration
docker-compose exec backend alembic upgrade head
```

## Internationalization (i18n)

### Adding Translations
1. Add keys to `frontend/messages/en.json`
2. Add French translations to `frontend/messages/fr-ca.json`
3. Use in components:
```typescript
import { useTranslations } from 'next-intl';

function MyComponent() {
  const t = useTranslations('dashboard');
  return <h1>{t('title')}</h1>;
}
```

### Backend i18n
For API responses, consider user's `preferred_language` field.

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No unnecessary files committed

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Reporting Bugs

### Bug Report Template
```markdown
**Describe the bug**
Clear description

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., macOS 12.0]
- Browser: [e.g., Chrome 96]
- Docker version:
```

## Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Alternative solutions

**Additional context**
Any other context
```

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly
5. Merge to main
6. Tag release
7. Deploy

## Questions?

- Open an issue
- Check existing documentation
- Review closed issues

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Your contributions make Biz-Bot better for everyone. Thank you for taking the time to contribute! 🎉
