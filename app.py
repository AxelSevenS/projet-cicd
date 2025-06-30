import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import time

is_debug = os.getenv('FLASK_DEBUG', '0') == '1'
log_level = logging.getLevelNamesMapping().get(os.getenv('LOG_LEVEL', 'INFO'), logging.INFO)
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=log_level)

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Security headers configuration
csp = {
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

# Initialize Talisman with security headers
talisman = Talisman(
    app,
    force_https=False,  # Set to True in production
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'style-src'],
    feature_policy={
        'geolocation': "'none'",
        'camera': "'none'",
        'microphone': "'none'",
        'payment': "'none'"
    }
)

# Add custom security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return render_template('error.html',
                         error_code=400,
                         error_message="Requête invalide"), 400

@app.errorhandler(403)
def forbidden(error):
    """Handle forbidden errors"""
    return render_template('error.html',
                         error_code=403,
                         error_message="Accès interdit"), 403

@app.errorhandler(404)
def page_not_found(error):
    """Handle page not found errors"""
    return render_template('error.html',
                         error_code=404,
                         error_message="Page non trouvée"), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit exceeded errors"""
    return render_template('error.html',
                         error_code=429,
                         error_message="Trop de requêtes. Veuillez réessayer plus tard."), 429

@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    logging.error(f"Internal server error: {error}")
    return render_template('error.html',
                         error_code=500,
                         error_message="Erreur interne du serveur"), 500

# Routes
@app.route('/')
def index():
    """Homepage with compelling environmental message"""
    return render_template('index.html')

@app.route('/info')
def info():
    """Information page with environmental data and statistics"""
    return render_template('info.html')

@app.route('/quiz')
def quiz():
    """Interactive quiz for environmental education"""
    return render_template('quiz.html')

@app.route('/actions')
def actions():
    """Action page with practical daily eco-friendly tips"""
    return render_template('actions.html')

@app.route('/share')
def share():
    """Share page with social media integration"""
    return render_template('share.html')

@app.route('/api/quiz/submit', methods=['POST'])
@limiter.limit("10 per minute")
def submit_quiz():
    """Handle quiz submission and return results"""
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400

        data = request.get_json()

        # Input validation
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        answers = data.get('answers', {})

        # Validate answers structure
        if not isinstance(answers, dict):
            return jsonify({'success': False, 'error': 'Invalid answers format'}), 400

        # Validate required questions
        required_questions = ['q1', 'q2', 'q3', 'q4', 'q5']
        for question in required_questions:
            if question not in answers:
                return jsonify({'success': False, 'error': f'Missing answer for {question}'}), 400

            # Validate answer values (must be a, b, c, or d)
            if answers[question] not in ['a', 'b', 'c', 'd']:
                return jsonify({'success': False, 'error': f'Invalid answer value for {question}'}), 400

        # Validate timeElapsed if provided
        time_elapsed = data.get('timeElapsed', 0)
        if not isinstance(time_elapsed, (int, float)) or time_elapsed < 0:
            time_elapsed = 0

        # Quiz scoring logic
        correct_answers = {
            'q1': 'b',  # 8 million tons of plastic
            'q2': 'c',  # 14% of greenhouse gases
            'q3': 'a',  # 1/3 of food produced
            'q4': 'b',  # LED bulbs use 80% less energy
            'q5': 'c'   # Transport accounts for 24% of emissions
        }

        score = 0
        total_questions = len(correct_answers)

        for question, correct_answer in correct_answers.items():
            if answers.get(question) == correct_answer:
                score += 1

        percentage = (score / total_questions) * 100

        # Generate personalized message based on score
        if percentage >= 80:
            message = "Excellent! Vous êtes un vrai champion de l'environnement! 🌟"
            level = "Expert Écologique"
        elif percentage >= 60:
            message = "Très bien! Vous avez de bonnes connaissances environnementales! 🌱"
            level = "Gardien de la Nature"
        elif percentage >= 40:
            message = "Pas mal! Il y a encore quelques points à améliorer. 🌿"
            level = "Apprenti Écolo"
        else:
            message = "C'est un début! Explorez notre site pour en apprendre plus! 🌍"
            level = "Novice Vert"

        return jsonify({
            'success': True,
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'message': message,
            'level': level
        })

    except Exception as e:
        logging.error(f"Quiz submission error: {e}")
        return jsonify({'success': False, 'error': 'Une erreur est survenue'}), 500

def start():
    # Get host and port from environment variables for better security
    host = os.environ.get('FLASK_HOST', '127.0.0.1')  # Default to localhost for security
    port = int(os.environ.get('FLASK_PORT', 5000))

    app.run(host=host, port=port, debug=is_debug)

if __name__ == '__main__':
    start()