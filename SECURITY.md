# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Updates

### Latest Security Fixes (2026-02-11)

The following vulnerabilities have been addressed by upgrading dependencies:

#### Backend (Python)
- **FastAPI**: Upgraded from 0.109.0 to 0.115.0
  - Fixed: ReDoS vulnerability in Content-Type header parsing
  - CVE: Duplicate Advisory for FastAPI Content-Type Header ReDoS

- **python-multipart**: Upgraded from 0.0.6 to 0.0.22
  - Fixed: Arbitrary File Write via Non-Default Configuration
  - Fixed: Denial of Service (DoS) via malformed multipart/form-data boundary
  - Fixed: Content-Type Header ReDoS vulnerability

#### Frontend (JavaScript/TypeScript)
- **Next.js**: Upgraded from 14.1.0 to 15.0.8
  - Fixed: HTTP request deserialization DoS when using insecure React Server Components
  - Patched multiple vulnerability vectors across different version ranges

## Reporting a Vulnerability

If you discover a security vulnerability in Biz-Bot, please follow these steps:

### 1. Do Not Open a Public Issue
Please do not open a public GitHub issue for security vulnerabilities.

### 2. Report via GitHub Security Advisories
1. Go to the repository's Security tab
2. Click "Report a vulnerability"
3. Fill in the details using the template below

### 3. Email (Alternative)
If you prefer, you can email security concerns to the maintainers.

### Vulnerability Report Template

```
**Vulnerability Type:**
[e.g., SQL Injection, XSS, CSRF, etc.]

**Affected Component:**
[e.g., Backend API, Frontend, Authentication system]

**Severity:**
[Critical / High / Medium / Low]

**Description:**
[Detailed description of the vulnerability]

**Steps to Reproduce:**
1. [First Step]
2. [Second Step]
3. [...]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Potential Impact:**
[What could an attacker do with this vulnerability?]

**Suggested Fix:**
[If you have suggestions]

**Environment:**
- Biz-Bot Version: [e.g., 1.0.0]
- Operating System: [e.g., Ubuntu 22.04]
- Browser (if applicable): [e.g., Chrome 96]
```

## Response Timeline

- **Initial Response**: Within 48 hours
- **Vulnerability Assessment**: Within 7 days
- **Fix Development**: Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: 90 days

## Security Best Practices

### For Deployment

1. **Environment Variables**
   - Never commit `.env` files
   - Use strong, unique values for `SECRET_KEY` and `MAGIC_LINK_SECRET`
   - Rotate secrets regularly

2. **API Keys**
   - Keep Twilio and ElevenLabs API keys secure
   - Use environment-specific keys
   - Implement rate limiting

3. **Database**
   - Use strong PostgreSQL passwords
   - Enable SSL/TLS for database connections
   - Regular backups with encryption

4. **Redis**
   - Enable password authentication
   - Use TLS for connections
   - Configure maxmemory policies

5. **Docker**
   - Keep base images updated
   - Use specific version tags
   - Scan images for vulnerabilities

6. **CORS**
   - Configure allowed origins properly
   - Don't use `*` in production
   - Validate Origin headers

### For Development

1. **Dependencies**
   - Regularly run `pip list --outdated` and `npm outdated`
   - Review dependency changes before upgrading
   - Use lock files (`requirements.txt`, `package-lock.json`)

2. **Code Review**
   - All changes should be reviewed
   - Use automated security scanning
   - Follow OWASP guidelines

3. **Testing**
   - Write security-focused tests
   - Test authentication flows
   - Validate input sanitization

## Security Features

### Current Implementation

- ✅ **Authentication**: Magic link with JWT tokens
- ✅ **Authorization**: Tenant-based isolation
- ✅ **Data Protection**: SQL injection prevention via SQLAlchemy ORM
- ✅ **CORS**: Configurable cross-origin restrictions
- ✅ **Password Hashing**: Bcrypt with secure defaults
- ✅ **Token Expiration**: Time-limited magic links and access tokens
- ✅ **Environment Configuration**: Secrets via environment variables
- ✅ **Database Migrations**: Versioned schema changes

### Planned Enhancements

- [ ] Rate limiting on authentication endpoints
- [ ] Account lockout after failed attempts
- [ ] Audit logging for sensitive operations
- [ ] Two-factor authentication (2FA)
- [ ] API key management for programmatic access
- [ ] Content Security Policy (CSP) headers
- [ ] Automated vulnerability scanning in CI/CD

## Dependencies

We actively monitor and update dependencies for security vulnerabilities:

### Backend
- FastAPI: 0.115.0+ (patched ReDoS vulnerability)
- python-multipart: 0.0.22+ (patched multiple vulnerabilities)
- SQLAlchemy: 2.0.25+
- Other dependencies are regularly updated

### Frontend
- Next.js: 15.0.8+ (patched HTTP deserialization DoS)
- React: 18.2.0+
- Other dependencies are regularly updated

## Disclosure Policy

When a vulnerability is confirmed:

1. We develop and test a fix
2. We prepare a security advisory
3. We release the patched version
4. We publicly disclose the vulnerability after users have time to upgrade (typically 7-14 days)

## Security Hall of Fame

We appreciate security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged here (with their permission).

## Contact

For security-related questions:
- GitHub: Open a security advisory
- Email: security@biz-bot.example.com (update with actual contact)

## License

This security policy is part of the Biz-Bot project and follows the same license terms.

---

**Last Updated:** 2026-02-11  
**Next Review:** 2026-05-11
