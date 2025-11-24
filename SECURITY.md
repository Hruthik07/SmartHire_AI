# Security Best Practices for SmartHire AI

## Overview
This document outlines security considerations and best practices for the SmartHire AI application.

## API Key Management

### OpenAI API Key
- **NEVER** commit API keys to version control
- Store API keys in `.env` file (excluded from git via `.gitignore`)
- Use environment-specific API keys (development vs. production)
- Rotate API keys regularly
- Monitor API usage for anomalies

### Environment Variables
Copy `.env.example` to `.env` and fill in your actual credentials:
```bash
cp .env.example .env
# Edit .env with your actual values
```

## CORS Configuration

### Development
For local development, use:
```
ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

### Production
For production, **ALWAYS** specify exact allowed origins:
```
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**NEVER** use `*` (allow all origins) in production as this creates security vulnerabilities.

## File Upload Security

### Current Protections
1. **File Size Limits**: Maximum 10MB per file
2. **File Type Validation**: Only PDF, DOCX, DOC, and TXT files accepted
3. **Filename Sanitization**: Prevents path traversal attacks
4. **Empty File Detection**: Rejects zero-byte files

### Additional Recommendations
1. Consider virus scanning for uploaded files
2. Store uploaded files in a sandboxed directory
3. Implement rate limiting on upload endpoints
4. Add user authentication for production use

## Input Validation

### Current Protections
1. Job descriptions limited to 50,000 characters
2. Empty input detection and rejection
3. File extension validation
4. Resume text length validation

### Best Practices
- Always validate and sanitize user inputs
- Use parameterized queries if database is added
- Implement request size limits
- Add content-type validation

## API Security

### Rate Limiting
Consider implementing rate limiting to prevent abuse:
- Per IP address limits
- Per user limits (if authentication is added)
- Global rate limits

### Authentication & Authorization
For production deployment, add:
- User authentication (JWT, OAuth2, etc.)
- Role-based access control
- API key authentication for API endpoints

## Error Handling

### Current Implementation
- Sensitive error details are logged but not exposed to users
- Generic error messages returned to clients
- Detailed logging for debugging

### Best Practices
- Never expose stack traces to clients
- Log errors securely with appropriate detail
- Monitor error rates for security incidents
- Implement proper exception handling

## Data Privacy

### Resume Data
- Uploaded resumes contain PII (Personally Identifiable Information)
- Consider data retention policies
- Implement secure deletion of old resumes
- Add encryption for stored resumes in production

### Compliance
Consider compliance with:
- GDPR (if processing EU resident data)
- CCPA (if processing California resident data)
- Other regional data protection laws

## Deployment Security

### HTTPS
- **ALWAYS** use HTTPS in production
- Obtain valid SSL/TLS certificates
- Configure secure headers (HSTS, CSP, etc.)

### Environment Isolation
- Use separate environments for dev/staging/production
- Never use production credentials in development
- Implement proper secrets management (AWS Secrets Manager, Azure Key Vault, etc.)

### Monitoring
- Log all API requests
- Monitor for suspicious activity
- Set up alerts for security events
- Regular security audits

## Dependencies

### Security Updates
- Regularly update dependencies to patch vulnerabilities
- Monitor security advisories for used libraries
- Use tools like `safety` or `pip-audit` to scan for vulnerabilities

### Example Security Check
```bash
pip install safety
safety check
```

## Vulnerability Reporting

If you discover a security vulnerability, please report it to the maintainers privately before public disclosure.

## Regular Security Tasks

### Weekly
- Review application logs for anomalies
- Check API usage patterns

### Monthly
- Update dependencies with security patches
- Review and rotate API keys if needed
- Audit user access (if applicable)

### Quarterly
- Comprehensive security audit
- Penetration testing (for production)
- Review and update security policies

## Security Checklist for Production Deployment

- [ ] All environment variables properly configured
- [ ] CORS restricted to specific origins
- [ ] HTTPS enabled with valid certificates
- [ ] File upload limits properly configured
- [ ] Rate limiting implemented
- [ ] Authentication added (if multi-user)
- [ ] Error logging configured securely
- [ ] Data retention policy implemented
- [ ] Regular backups configured
- [ ] Security monitoring in place
- [ ] Dependencies updated to latest secure versions
- [ ] Security headers configured
- [ ] Input validation comprehensive
- [ ] API keys rotated and secured
