# Biz-Bot API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

Biz-Bot uses magic link authentication. No passwords required!

### Request Magic Link
Send a magic link to user's email.

**Endpoint:** `POST /api/v1/auth/request-magic-link`

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If the email exists, a magic link has been sent"
}
```

### Verify Magic Link
Exchange magic link token for access token.

**Endpoint:** `POST /api/v1/auth/verify-magic-link`

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Register User
Create a new user account.

**Endpoint:** `POST /api/v1/auth/register`

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "full_name": "Jane Doe",
  "tenant_id": 1,
  "preferred_language": "en"
}
```

**Response:**
```json
{
  "id": 1,
  "tenant_id": 1,
  "email": "newuser@example.com",
  "full_name": "Jane Doe",
  "is_active": true,
  "is_admin": false,
  "preferred_language": "en",
  "created_at": "2026-02-11T17:21:00Z"
}
```

## Health & Status

### Health Check
Check system health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "ok",
  "redis": "ok"
}
```

### Root Endpoint
Get API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "name": "Biz-Bot",
  "version": "1.0.0",
  "message": "Biz-Bot API is running"
}
```

## Bookings

All booking endpoints require authentication. Include the access token in the Authorization header:
```
Authorization: Bearer {access_token}
```

### List Bookings
Get all bookings for a tenant.

**Endpoint:** `GET /api/v1/bookings?tenant_id={tenant_id}&skip=0&limit=100`

**Query Parameters:**
- `tenant_id` (required): Tenant ID
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "tenant_id": 1,
    "customer_name": "Sophie Martin",
    "customer_email": "sophie@example.com",
    "customer_phone": "+1-514-555-0100",
    "service_type": "Table Reservation",
    "appointment_time": "2026-02-13T18:00:00Z",
    "status": "confirmed",
    "notes": "Table for 4 people, near window",
    "created_at": "2026-02-11T17:21:00Z"
  }
]
```

### Create Booking
Create a new booking.

**Endpoint:** `POST /api/v1/bookings`

**Request Body:**
```json
{
  "tenant_id": 1,
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+1-514-555-0123",
  "service_type": "Consultation",
  "appointment_time": "2026-02-15T14:00:00Z",
  "notes": "First time customer"
}
```

**Response:** Same as booking object above.

### Get Booking
Get details of a specific booking.

**Endpoint:** `GET /api/v1/bookings/{booking_id}`

**Response:** Same as booking object above.

### Update Booking
Update booking details.

**Endpoint:** `PUT /api/v1/bookings/{booking_id}`

**Request Body:**
```json
{
  "status": "confirmed",
  "notes": "Updated notes"
}
```

**Response:** Updated booking object.

### Delete Booking
Delete a booking.

**Endpoint:** `DELETE /api/v1/bookings/{booking_id}`

**Response:**
```json
{
  "message": "Booking deleted successfully"
}
```

## FAQs

### List FAQs
Get all FAQs for a tenant.

**Endpoint:** `GET /api/v1/faqs?tenant_id={tenant_id}&language=en&skip=0&limit=100`

**Query Parameters:**
- `tenant_id` (required): Tenant ID
- `language` (optional): Language code (en, fr-ca) (default: en)
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "tenant_id": 1,
    "question_en": "What are your opening hours?",
    "answer_en": "We are open Monday to Friday from 7 AM to 10 PM.",
    "question_fr": "Quelles sont vos heures d'ouverture?",
    "answer_fr": "Nous sommes ouverts du lundi au vendredi de 7h à 22h.",
    "category": "General",
    "is_active": true,
    "created_at": "2026-02-11T17:21:00Z"
  }
]
```

### Create FAQ
Create a new FAQ.

**Endpoint:** `POST /api/v1/faqs`

**Request Body:**
```json
{
  "tenant_id": 1,
  "question_en": "Do you accept credit cards?",
  "answer_en": "Yes, we accept all major credit cards.",
  "question_fr": "Acceptez-vous les cartes de crédit?",
  "answer_fr": "Oui, nous acceptons toutes les principales cartes de crédit.",
  "category": "Payment"
}
```

**Response:** Same as FAQ object above.

### Get FAQ
Get details of a specific FAQ.

**Endpoint:** `GET /api/v1/faqs/{faq_id}`

**Response:** Same as FAQ object above.

### Update FAQ
Update FAQ details.

**Endpoint:** `PUT /api/v1/faqs/{faq_id}`

**Request Body:**
```json
{
  "is_active": false
}
```

**Response:** Updated FAQ object.

### Delete FAQ
Delete an FAQ.

**Endpoint:** `DELETE /api/v1/faqs/{faq_id}`

**Response:**
```json
{
  "message": "FAQ deleted successfully"
}
```

## Tenants (Admin Only)

### List Tenants
Get all tenants in the system.

**Endpoint:** `GET /api/v1/tenants?skip=0&limit=100`

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Café Québécois",
    "slug": "cafe-quebecois",
    "is_active": true,
    "created_at": "2026-02-11T17:21:00Z"
  }
]
```

### Create Tenant
Create a new tenant.

**Endpoint:** `POST /api/v1/tenants`

**Request Body:**
```json
{
  "name": "My Business",
  "slug": "my-business"
}
```

**Response:** Same as tenant object above.

### Get Tenant
Get details of a specific tenant.

**Endpoint:** `GET /api/v1/tenants/{tenant_id}`

**Response:** Same as tenant object above.

## Error Responses

All endpoints may return error responses in the following format:

**400 Bad Request:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider implementing rate limiting based on your requirements.

## WebSocket Support

WebSocket support for real-time updates is not currently implemented but can be added for features like:
- Real-time booking notifications
- Live chat support
- System status updates

## Pagination

List endpoints support pagination with `skip` and `limit` query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 100)

## Internationalization

The API supports multiple languages through the `language` parameter where applicable:
- `en`: English
- `fr-ca`: French Canadian

FAQs can have both English and French versions stored in the same record.

## Interactive Documentation

FastAPI provides interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

These interfaces allow you to test all endpoints directly from your browser.
