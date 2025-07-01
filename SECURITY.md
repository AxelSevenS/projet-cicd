# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email [security@example.com](mailto:security@example.com). Do **not** create a public issue.

## Incident Response Plan

1. Take the application offline (Unpublish page [here]([Secrets](https://github.com/Rookuro/projet-cicd/settings/pages))).
2. Revoke credentials in repo ([Secrets](https://github.com/Rookuro/projet-cicd/settings/secrets/actions), [Variables](https://github.com/Rookuro/projet-cicd/settings/variables/actions)) and from sources (TBD, e.g., )
3. Analyze logs and isolate the issue.
4. Patch vulnerabilities and rotate secrets ([Secrets](https://github.com/Rookuro/projet-cicd/settings/secrets/actions), [Variables](https://github.com/Rookuro/projet-cicd/settings/variables/actions)).
5. Redeploy and monitor the system.

## Best Practices Followed

- HTTPS enforced across all endpoints
- Environment variables for secrets
- SQL injection protection (ORM & parameterized queries)
- Rate limiting and request validation
- Security headers (Content-Security-Policy, etc.)


# Security Implementation Guide

## Security Measures Implemented

### 1. Security Headers
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-Frame-Options**: Prevents clickjacking attacks
- **X-XSS-Protection**: Enables XSS filtering
- **Content Security Policy**: Restricts resource loading
- **Strict-Transport-Security**: Enforces HTTPS
- **Referrer-Policy**: Controls referrer information

### 2. Input Validation
- Strict validation of quiz submission data
- JSON schema validation for API endpoints
- Sanitization of user inputs
- Type checking and bounds validation

### 3. Rate Limiting
- API endpoint rate limiting (10 requests/minute for quiz)
- General rate limiting (200/day, 50/hour)
- Memory-based storage for development
- Redis recommended for production

### 4. Safe DOM Manipulation
- Replaced `innerHTML` with `textContent` and `createElement`
- Prevents XSS through DOM manipulation
- Proper escaping of dynamic content

### 5. Secure External Resources
- Subresource Integrity (SRI) for CDN resources
- Crossorigin attributes for security
- CSP restrictions on external resources

### 6. Error Handling
- Custom error pages for common HTTP errors
- Secure error messages without sensitive information
- Proper logging of security events

### 7. Production Security
- Environment-based host binding
- HTTPS enforcement in production
- Debug mode disabled by default

## Deployment Security Checklist

### Before Production Deployment:

1. **Environment Variables**
   ```bash
   export FLASK_DEBUG=0
   export FLASK_HOST=0.0.0.0
   export FORCE_HTTPS=true
   ```

2. **Install Security Dependencies**
   ```bash
   pip install flask-talisman flask-limiter
   ```

3. **Update CSP for Production**
   - Remove `'unsafe-inline'` if possible
   - Use nonces for inline scripts
   - Minimize external domains

4. **Configure Reverse Proxy**
   - Use Nginx/Apache with security headers
   - Enable HTTPS with proper certificates
   - Configure proper firewall rules

5. **Monitor Security**
   - Set up logging for security events
   - Monitor rate limiting violations
   - Regular security audits

### Security Headers Verification

You can verify security headers using:
- [SecurityHeaders.com](https://securityheaders.com)
- [Mozilla Observatory](https://observatory.mozilla.org)

### Recommended Production Setup

```nginx
# Nginx configuration example
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Testing

### Manual Testing
1. Check security headers in browser developer tools
2. Test rate limiting by making multiple requests
3. Verify error pages don't expose sensitive information
4. Test XSS prevention with malicious inputs

### Automated Testing
```bash
# Security scanning tools
pip install bandit safety
bandit -r . -f json
safety check
```

## Security Monitoring

### Log Security Events
- Failed authentication attempts
- Rate limit violations
- Input validation failures
- Suspicious request patterns

### Alerts Setup
- Monitor for unusual traffic patterns
- Alert on security header bypass attempts
- Track error rates and types

## Regular Security Maintenance

1. **Update Dependencies**
   - Regular security updates
   - Vulnerability scanning
   - Dependency audits

2. **Security Reviews**
   - Quarterly security assessments
   - Code reviews for security
   - Penetration testing

3. **Configuration Updates**
   - Review CSP policies
   - Update rate limits as needed
   - Refresh security headers

## Incident Response

If security incident occurs:
1. Immediately revoke compromised secrets
2. Update security configurations
3. Analyze logs for breach scope
4. Implement additional security measures
5. Document lessons learned

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
