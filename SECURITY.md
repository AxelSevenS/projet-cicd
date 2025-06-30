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
