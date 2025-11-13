from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

# ============================================================================
# APPLICATION FACTORY
# ============================================================================

def create_app(config_name=None):
    """Application factory pattern for better testing and configuration"""
    app = Flask(__name__)
    
    # Load configuration
    configure_app(app, config_name)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure logging
    configure_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints (routes)
    register_routes(app)
    
    return app

def configure_app(app, config_name=None):
    """Configure the Flask application"""
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    database_uri = os.environ.get('DATABASE_URL', 'sqlite:///vidensbank.db')
    # Fix Heroku postgres:// to postgresql://
    if database_uri.startswith('postgres://'):
        database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Security headers
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    
    # File upload configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    
    # Application settings
    app.config['APP_NAME'] = os.environ.get('APP_NAME', 'Vidensbank')
    
    return app

def configure_logging(app):
    """Configure application logging"""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # File handler
        file_handler = RotatingFileHandler(
            'logs/vidensbank.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Vidensbank startup')

def register_error_handlers(app):
    """Register error handlers"""
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f'Server Error: {e}')
        return render_template('500.html'), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(e):
        flash('Filen er for stor. Maksimal størrelse er 16MB.', 'error')
        return redirect(request.url), 413

def register_routes(app):
    """Register all application routes"""
    # Import routes here to avoid circular imports
    with app.app_context():
        from routes import register_all_routes
        register_all_routes(app)

# ============================================================================
# INITIALIZE EXTENSIONS
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
database_uri = os.environ.get('DATABASE_URL', 'sqlite:///vidensbank.db')
if database_uri.startswith('postgres://'):
    database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin, editor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')  # new, read, replied

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================================================
# CONTEXT PROCESSORS
# ============================================================================

@app.context_processor
def inject_current_year():
    """Inject current year and app config into all templates"""
    return {
        'current_year': datetime.now().year,
        'app_name': app.config.get('APP_NAME', 'Vidensbank')
    }

# ============================================================================
# SECURITY HEADERS
# ============================================================================

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    # Prevent XSS attacks
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # HTTPS enforcement (production only)
    if app.config.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://fonts.cdnfonts.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.cdnfonts.com; "
        "font-src 'self' https://fonts.gstatic.com https://fonts.cdnfonts.com; "
        "img-src 'self' data: https:; "
    )
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # Cache control for static assets
    if request.path.startswith('/static/'):
        # Cache static files for 1 year
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    elif request.path in ['/', '/index']:
        # Cache homepage for 1 hour
        response.headers['Cache-Control'] = 'public, max-age=3600'
    else:
        # Don't cache dynamic content
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    return response

@app.before_request
def log_request_info():
    """Log request information for monitoring"""
    if not app.debug:
        app.logger.info(f'{request.method} {request.path} from {request.remote_addr}')

# ============================================================================
# HEALTH CHECK & MONITORING
# ============================================================================

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
        app.logger.error(f'Health check failed: {e}')
    
    health_data = {
        'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
    
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return jsonify(health_data), status_code

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'online',
        'api_version': '1.0',
        'endpoints': {
            'calculate_co2': '/api/calculate-co2',
            'search': '/search',
            'health': '/health'
        }
    })

# ============================================================================
# ROUTES - PUBLIC PAGES
# ============================================================================

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/emissioner-og-baeredygtighed')
def emissions_sustainability():
    return render_template('emissions/main.html')

@app.route('/emissioner-og-baeredygtighed/fodevare-relaterede-emissioner')
def food_emissions():
    return render_template('emissions/food_emissions.html')

@app.route('/emissioner-og-baeredygtighed/datadrevet-tilgang')
def data_driven_approach():
    return render_template('emissions/data_driven_approach.html')

@app.route('/emissioner-og-baeredygtighed/branchepraestation')
def market_analysis():
    return render_template('emissions/market_analysis.html')

@app.route('/emissioner-og-baeredygtighed/politisk-landskab')
def political_landscape():
    return render_template('emissions/political_landscape.html')

@app.route('/emissioner-og-baeredygtighed/klimadata')
def climate_data():
    return render_template('emissions/climate_data.html')

@app.route('/oekologi')
def ecology():
    return render_template('ecology/main.html')

# Økologi routes
@app.route('/okologi')
def okologi():
    return render_template('okologi/index.html')

@app.route('/okologi/hvad-er')
def okologi_hvad_er():
    return render_template('okologi/okologi_hvad_er.html')

@app.route('/okologi/regulering')
def okologi_regulering():
    return render_template('okologi/okologi_regulering.html')

@app.route('/okologi/kantinen')
def okologi_kantinen():
    return render_template('okologi/okologi_kantinen.html')

@app.route('/okologi/fordele')
def okologi_fordele():
    return render_template('okologi/okologi_fordele.html')

@app.route('/okologi/nuanceret')
def okologi_nuanceret():
    return render_template('okologi/okologi_nuanceret.html')

@app.route('/okologi/esg')
def okologi_esg():
    return render_template('okologi/okologi_esg.html')

# ============================================================================
# CO2 CALCULATOR
# ============================================================================

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/api/calculate-co2', methods=['POST'])
def calculate_co2():
    """API endpoint for CO2 calculations with error handling"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        food_type = data.get('food_type', '')
        quantity = data.get('quantity', 0)
        
        # Validate inputs
        if not food_type:
            return jsonify({'success': False, 'error': 'food_type is required'}), 400
        
        try:
            quantity = float(quantity)
            if quantity < 0:
                return jsonify({'success': False, 'error': 'quantity must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid quantity value'}), 400
        
        # CO2 emissions per kg (kg CO2e per kg food)
        emission_factors = {
            'beef': 27.0,
            'lamb': 39.2,
            'pork': 12.1,
            'chicken': 6.9,
            'turkey': 10.9,
            'fish': 5.0,
            'shrimp': 11.8,
            'cheese': 13.5,
            'milk': 1.9,
            'eggs': 4.8,
            'vegetables': 2.0,
            'potatoes': 0.5,
            'rice': 4.0,
            'grains': 1.5,
            'beans': 2.0,
            'nuts': 2.3
        }
        
        co2_per_kg = emission_factors.get(food_type.lower(), 5.0)
        total_co2 = quantity * co2_per_kg
        
        # Calculate equivalents for context
        car_km_equivalent = total_co2 / 0.12  # Average car emits 0.12 kg CO2/km
        tree_months = total_co2 / 0.006  # One tree absorbs ~0.006 kg CO2/day
        
        response = {
            'success': True,
            'co2_emissions': round(total_co2, 2),
            'food_type': food_type,
            'quantity': quantity,
            'unit': 'kg CO2e',
            'equivalents': {
                'car_km': round(car_km_equivalent, 2),
                'trees_days': round(tree_months, 1)
            }
        }
        
        app.logger.info(f'CO2 calculation: {food_type} {quantity}kg = {total_co2}kg CO2e')
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f'Error in CO2 calculation: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

# ============================================================================
# SEARCH FUNCTIONALITY
# ============================================================================

@app.route('/search')
def search():
    """Enhanced search with pagination and better error handling"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    results = []
    pagination = None
    
    if query:
        try:
            # Search in page titles and content
            search_query = Page.query.filter(
                db.or_(
                    Page.title.ilike(f'%{query}%'),
                    Page.content.ilike(f'%{query}%')
                ),
                Page.is_published == True
            )
            
            pagination = search_query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            results = pagination.items
            
            app.logger.info(f'Search for "{query}" returned {len(results)} results')
        except Exception as e:
            app.logger.error(f'Search error: {e}')
            flash('Der opstod en fejl under søgningen. Prøv igen.', 'error')
    
    return render_template('search_results.html', 
                         query=query, 
                         results=results,
                         pagination=pagination)

# ============================================================================
# CONTACT FORM
# ============================================================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Enhanced contact form with validation and spam protection"""
    if request.method == 'POST':
        try:
            # Validate required fields
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            
            # Basic validation
            if not all([name, email, subject, message]):
                flash('Alle felter skal udfyldes.', 'error')
                return redirect(url_for('contact'))
            
            # Email format validation (basic)
            if '@' not in email or '.' not in email:
                flash('Indtast en gyldig email adresse.', 'error')
                return redirect(url_for('contact'))
            
            # Create contact entry
            contact = ContactForm(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact)
            db.session.commit()
            
            app.logger.info(f'New contact form submission from {email}')
            flash('Tak for din besked! Vi vender tilbage hurtigst muligt.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Contact form error: {e}')
            flash('Der opstod en fejl. Prøv igen senere.', 'error')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')

# ============================================================================
# AUTHENTICATION
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Enhanced login with rate limiting consideration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Brugernavn og adgangskode er påkrævet.', 'error')
                return redirect(url_for('login'))
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                
                # Validate next_page to prevent open redirects
                if next_page and next_page.startswith('/'):
                    app.logger.info(f'User {username} logged in successfully')
                    return redirect(next_page)
                return redirect(url_for('dashboard'))
            else:
                app.logger.warning(f'Failed login attempt for username: {username}')
                flash('Ugyldigt brugernavn eller adgangskode', 'error')
        except Exception as e:
            app.logger.error(f'Login error: {e}')
            flash('Der opstod en fejl. Prøv igen.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Enhanced registration with better validation"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            password_confirm = request.form.get('password_confirm', '')
            
            # Validation
            if not all([username, email, password]):
                flash('Alle felter skal udfyldes', 'error')
                return redirect(url_for('register'))
            
            if len(username) < 3:
                flash('Brugernavn skal være mindst 3 tegn', 'error')
                return redirect(url_for('register'))
            
            if len(password) < 8:
                flash('Adgangskode skal være mindst 8 tegn', 'error')
                return redirect(url_for('register'))
            
            if password != password_confirm:
                flash('Adgangskoderne matcher ikke', 'error')
                return redirect(url_for('register'))
            
            if User.query.filter_by(username=username).first():
                flash('Brugernavn eksisterer allerede', 'error')
                return redirect(url_for('register'))
            
            if User.query.filter_by(email=email).first():
                flash('Email er allerede registreret', 'error')
                return redirect(url_for('register'))
            
            # Create user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            app.logger.info(f'New user registered: {username}')
            flash('Registrering gennemført! Du kan nu logge ind.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Registration error: {e}')
            flash('Der opstod en fejl. Prøv igen senere.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

# ============================================================================
# USER DASHBOARD (Protected)
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Du har ikke adgang til denne side', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    pages = Page.query.all()
    contacts = ContactForm.query.order_by(ContactForm.submitted_at.desc()).all()
    
    return render_template('admin.html', users=users, pages=pages, contacts=contacts)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    app.logger.warning(f'404 error: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f'500 error: {e}')
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(e):
    app.logger.warning(f'403 error: {request.url}')
    flash('Du har ikke tilladelse til at tilgå denne side.', 'error')
    return redirect(url_for('index')), 403

@app.errorhandler(413)
def request_entity_too_large(e):
    flash('Filen er for stor. Maksimal størrelse er 16MB.', 'error')
    return redirect(url_for('index')), 413

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def create_admin():
    """Create an admin user."""
    admin = User(username='admin', email='admin@vidensbank.dk', role='admin')
    admin.set_password('admin123')  # Change this in production!
    db.session.add(admin)
    db.session.commit()
    print('Admin user created! Username: admin, Password: admin123')

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
