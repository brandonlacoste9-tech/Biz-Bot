# Biz-Bot API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Get Access Token

**Magic Link Flow:**
1. Request magic link: `POST /auth/magic-link/request`
2. Check email for magic link
3. Click link or use token to verify: `POST /auth/magic-link/verify`
4. Receive JWT token

---

## Health Endpoints

### GET /health/
Basic health check.

**Response:**
```json
{
  "status": "healthy",
  "service": "Biz-Bot API"
}
```

### GET /health/ready
Readiness check with database connectivity.

**Response:**
```json
{
  "status": "ready",
  "database": "connected"
}
```

### GET /health/live
Liveness check.

**Response:**
```json
{
  "status": "alive"
}
```

---

## Authentication Endpoints

### POST /auth/magic-link/request
Request a magic link for authentication.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Magic link sent to your email"
}
```

### POST /auth/magic-link/verify
Verify magic link token and get access token.

**Request Body:**
```json
{
  "token": "your_magic_link_token"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "tenant_id": "tenant_uuid",
    "is_active": true,
    "is_admin": false,
    "language": "en",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  },
  "tenant": {
    "id": "uuid",
    "name": "Business Name",
    "slug": "business-slug",
    "email": "business@example.com",
    "phone": "+1234567890",
    "is_active": true,
    "settings": {},
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### GET /auth/me
Get current authenticated user. Requires authentication.

**Response:** Same as verify endpoint

---

## Tenant Endpoints

### POST /tenants/
Create a new tenant.

**Request Body:**
```json
{
  "name": "My Business",
  "slug": "my-business",
  "email": "contact@mybusiness.com",
  "phone": "+15141234567",
  "settings": {}
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "My Business",
  "slug": "my-business",
  "email": "contact@mybusiness.com",
  "phone": "+15141234567",
  "is_active": true,
  "settings": {},
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### GET /tenants/{tenant_id}
Get tenant by ID. Requires authentication.

**Response:** Same as create tenant

### PATCH /tenants/{tenant_id}
Update tenant. Requires authentication.

**Request Body:**
```json
{
  "name": "Updated Business Name",
  "phone": "+15149876543",
  "settings": {"key": "value"}
}
```

**Response:** Updated tenant object

### GET /tenants/
List all tenants. Requires admin authentication.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Business Name",
    ...
  }
]
```

---

## Booking Endpoints

### POST /bookings/
Create a new booking. Public endpoint (no auth required).

**Request Body:**
```json
{
  "tenant_id": "tenant_uuid",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+15141234567",
  "service_type": "Consultation",
  "appointment_date": "2024-01-15T10:00:00",
  "notes": "Additional notes",
  "source": "web"
}
```

**Response:**
```json
{
  "id": "uuid",
  "tenant_id": "tenant_uuid",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+15141234567",
  "service_type": "Consultation",
  "appointment_date": "2024-01-15T10:00:00",
  "status": "pending",
  "notes": "Additional notes",
  "source": "web",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### GET /bookings/
List bookings for current tenant. Requires authentication.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)
- `status`: Filter by status (pending, confirmed, cancelled, completed)

**Response:** Array of booking objects

### GET /bookings/{booking_id}
Get booking by ID. Requires authentication.

**Response:** Booking object

### PATCH /bookings/{booking_id}
Update booking. Requires authentication.

**Request Body:**
```json
{
  "status": "confirmed",
  "appointment_date": "2024-01-16T14:00:00",
  "notes": "Updated notes"
}
```

**Response:** Updated booking object

### DELETE /bookings/{booking_id}
Delete booking. Requires authentication.

**Response:** 204 No Content

---

## FAQ Endpoints

### POST /faq/
Create a new FAQ item. Requires authentication.

**Request Body:**
```json
{
  "tenant_id": "tenant_uuid",
  "question_en": "What are your hours?",
  "question_fr": "Quelles sont vos heures?",
  "answer_en": "We are open 9-5 Monday to Friday",
  "answer_fr": "Nous sommes ouverts de 9h à 17h du lundi au vendredi",
  "keywords": ["hours", "heures", "open"],
  "order": 1
}
```

**Response:**
```json
{
  "id": "uuid",
  "tenant_id": "tenant_uuid",
  "question_en": "What are your hours?",
  "question_fr": "Quelles sont vos heures?",
  "answer_en": "We are open 9-5 Monday to Friday",
  "answer_fr": "Nous sommes ouverts de 9h à 17h du lundi au vendredi",
  "keywords": ["hours", "heures", "open"],
  "is_active": true,
  "order": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### GET /faq/
List FAQ items. Public endpoint.

**Query Parameters:**
- `tenant_id`: Filter by tenant
- `language`: Filter by language (en, fr)
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)

**Response:** Array of FAQ objects

### GET /faq/search
Search FAQ items. Public endpoint.

**Query Parameters:**
- `q`: Search query (required)
- `tenant_id`: Tenant ID (required)
- `language`: Language (en or fr, default: en)

**Response:**
```json
{
  "results": [
    {
      "id": "uuid",
      "question": "What are your hours?",
      "answer": "We are open 9-5 Monday to Friday"
    }
  ]
}
```

### GET /faq/{faq_id}
Get FAQ item by ID. Public endpoint.

**Response:** FAQ object

### PATCH /faq/{faq_id}
Update FAQ item. Requires authentication.

**Request Body:**
```json
{
  "question_en": "Updated question",
  "answer_en": "Updated answer",
  "is_active": true
}
```

**Response:** Updated FAQ object

### DELETE /faq/{faq_id}
Delete FAQ item. Requires authentication.

**Response:** 204 No Content

---

## Admin Endpoints

All admin endpoints require admin authentication.

### GET /admin/stats
Get platform statistics.

**Response:**
```json
{
  "tenants": {
    "total": 10,
    "active": 8
  },
  "users": {
    "total": 45
  },
  "bookings": {
    "total": 150
  },
  "faqs": {
    "total": 75
  }
}
```

### GET /admin/users
List all users.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)

**Response:** Array of user objects

### GET /admin/tenants
List all tenants.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)

**Response:** Array of tenant objects

---

## Webhook Endpoints

### POST /webhooks/twilio/sms
Handle incoming SMS from Twilio.

**Request:** Twilio SMS webhook format

**Response:** TwiML response

### POST /webhooks/twilio/whatsapp
Handle incoming WhatsApp messages from Twilio.

**Request:** Twilio WhatsApp webhook format

**Response:** TwiML response

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to access this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting for public endpoints.

## CORS

CORS is configured to allow requests from `http://localhost:3000` in development. Update `FRONTEND_URL` in `.env` for production.

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.
