"""
Security configuration for EcoAlerte
"""

import os

class SecurityConfig:
    """Security configuration settings"""

    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    }

    # Content Security Policy
    CSP_CONFIG = {
        'default-src': "'self'",
        'script-src': [
            "'self'",
            "'unsafe-inline'",  # Required for Bootstrap and Chart.js inline scripts
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com"
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline styles
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://fonts.googleapis.com"
        ],
        'font-src': [
            "'self'",
            "https://fonts.gstatic.com",
            "https://cdnjs.cloudflare.com"
        ],
        'img-src': [
            "'self'",
            "data:",
            "https:"
        ],
        'connect-src': "'self'"
    }

    # Rate Limiting Configuration
    RATE_LIMIT_CONFIG = {
        'default_limits': ["200 per day", "50 per hour"],
        'api_limits': {
            'quiz_submit': "10 per minute"
        }
    }

    # Feature Policy
    FEATURE_POLICY = {
        'geolocation': "'none'",
        'camera': "'none'",
        'microphone': "'none'",
        'payment': "'none'"
    }

    # Production Security Settings
    PRODUCTION_CONFIG = {
        'force_https': True,
        'strict_transport_security': True,
        'strict_transport_security_max_age': 31536000  # 1 year
    }

    @staticmethod
    def get_host():
        """Get host configuration based on environment"""
        if os.environ.get('FLASK_ENV') == 'production':
            return os.environ.get('FLASK_HOST', '0.0.0.0')
        return os.environ.get('FLASK_HOST', '127.0.0.1')

    @staticmethod
    def should_force_https():
        """Check if HTTPS should be forced"""
        return os.environ.get('FLASK_ENV') == 'production'

    @staticmethod
    def get_allowed_origins():
        """Get allowed origins for CORS if needed"""
        origins = os.environ.get('ALLOWED_ORIGINS', '')
        if origins:
            return origins.split(',')
        return []

# Input validation schemas
QUIZ_VALIDATION_SCHEMA = {
    'type': 'object',
    'required': ['answers'],
    'properties': {
        'answers': {
            'type': 'object',
            'required': ['q1', 'q2', 'q3', 'q4', 'q5'],
            'properties': {
                'q1': {'type': 'string', 'enum': ['a', 'b', 'c', 'd']},
                'q2': {'type': 'string', 'enum': ['a', 'b', 'c', 'd']},
                'q3': {'type': 'string', 'enum': ['a', 'b', 'c', 'd']},
                'q4': {'type': 'string', 'enum': ['a', 'b', 'c', 'd']},
                'q5': {'type': 'string', 'enum': ['a', 'b', 'c', 'd']}
            },
            'additionalProperties': False
        },
        'timeElapsed': {
            'type': 'number',
            'minimum': 0,
            'maximum': 3600  # Max 1 hour
        }
    },
    'additionalProperties': False
}
