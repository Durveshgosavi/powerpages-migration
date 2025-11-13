# 🌱 Vidensbank Flask Application

A modern Flask web application for sustainability, climate data, and food innovation - migrated from Microsoft Power Pages.

[![Deploy to Heroku](https://img.shields.io/badge/deploy-heroku-purple.svg)](https://heroku.com/deploy)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- ✅ **User Authentication** - Secure login, registration, and role-based access
- ✅ **CO2 Calculator** - Interactive API for carbon footprint calculations
- ✅ **Search Functionality** - Full-text search with pagination
- ✅ **Contact Forms** - Secure form submissions with validation
- ✅ **Responsive Design** - Mobile-first design with flip cards and KPI dashboards
- ✅ **Admin Panel** - Content management and user administration
- ✅ **PostgreSQL Support** - Production-ready database configuration
- ✅ **Health Check API** - Monitoring and status endpoints
- ✅ **Security** - CSRF protection, secure sessions, input validation
- ✅ **CI/CD Ready** - GitHub Actions for automated deployment
- ✅ **Heroku Optimized** - One-click deployment with Procfile

## 🛠 Technology Stack

**Backend:**
- Python 3.12
- Flask 3.0
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- PostgreSQL (Production) / SQLite (Development)

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5
- Responsive Grid Layout
- CSS Custom Properties

**Deployment:**
- Heroku
- Gunicorn (WSGI Server)
- GitHub Actions (CI/CD)

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Local Development](#-local-development)
- [Environment Configuration](#-environment-configuration)
- [Heroku Deployment](#-heroku-deployment)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)

## 💻 Local Development

### Prerequisites

- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **PostgreSQL** (Optional for local development) - [Download](https://www.postgresql.org/)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Durveshgosavi/powerpages-migration.git
   cd powerpages-migration
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env and set your configuration
   # At minimum, set a secure SECRET_KEY
   ```

5. **Initialize database**
   ```bash
   flask init-db
   ```

6. **Create admin user (optional)**
   ```bash
   flask create-admin
   ```
   Default credentials:
   - **Username:** admin
   - **Password:** admin123 (⚠️ Change in production!)

7. **Run the application**
   ```bash
   # Development mode
   python app.py
   
   # Or use Flask CLI
   flask run
   ```

8. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 🔐 Environment Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and configure:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Database connection string | `sqlite:///vidensbank.db` or PostgreSQL URL |
| `FLASK_ENV` | Environment mode | `development` or `production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Enable debug mode | `True` in development |
| `APP_NAME` | Application name | `Vidensbank` |
| `BASE_URL` | Base URL for the app | `http://localhost:5000` |
| `ADMIN_EMAIL` | Admin notification email | None |

See `.env.example` for full configuration options.

## 🚀 Heroku Deployment

### Method 1: GitHub Integration (Recommended)

1. **Fork/Clone this repository to your GitHub account**

2. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
   heroku config:set FLASK_ENV=production
   heroku config:set SESSION_COOKIE_SECURE=True
   ```

5. **Deploy via GitHub**
   - Go to Heroku Dashboard → Your App → Deploy
   - Connect to GitHub and select your repository
   - Enable automatic deploys (optional)
   - Click "Deploy Branch"

6. **Initialize database**
   ```bash
   heroku run flask init-db
   heroku run flask create-admin
   ```

7. **Open your app**
   ```bash
   heroku open
   ```

### Method 2: Git Push

```bash
# Login to Heroku
heroku login

# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy
git push heroku main

# Initialize database
heroku run flask init-db
```

### Method 3: GitHub Actions (CI/CD)

This repository includes GitHub Actions workflows for automated deployment:

1. **Add secrets to your GitHub repository:**
   - Go to Settings → Secrets and variables → Actions
   - Add these secrets:
     - `HEROKU_API_KEY` - Your Heroku API key
     - `HEROKU_APP_NAME` - Your Heroku app name
     - `HEROKU_EMAIL` - Your Heroku account email

2. **Push to main branch:**
   ```bash
   git push origin main
   ```

3. **GitHub Actions will automatically:**
   - Run tests
   - Check code quality
   - Deploy to Heroku
   - Run health checks

### Heroku Configuration

**Required Buildpacks:**
```bash
heroku buildpacks:set heroku/python
```

**Scale dynos:**
```bash
heroku ps:scale web=1
```

**View logs:**
```bash
heroku logs --tail
```

**Restart app:**
```bash
heroku restart
```

## 📖 Usage

### Admin Panel

1. Log in with admin credentials
2. Navigate to `/admin`
3. Manage:
   - Users and permissions
   - Content pages
   - Contact form submissions

### CO2 Calculator

Access the calculator at `/calculator` or use the API endpoint directly:

```javascript
fetch('/api/calculate-co2', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    food_type: 'beef',
    quantity: 1.5
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Search

Use the search bar in the navigation or access `/search?q=query`

## 🔌 API Documentation

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "2025-11-13T10:30:00.000000",
  "version": "1.0.0"
}
```

### API Status

**Endpoint:** `GET /api/status`

**Response:**
```json
{
  "status": "online",
  "api_version": "1.0",
  "endpoints": {
    "calculate_co2": "/api/calculate-co2",
    "search": "/search",
    "health": "/health"
  }
}
```

### Calculate CO2

**Endpoint:** `POST /api/calculate-co2`

**Request:**
```json
{
  "food_type": "beef",
  "quantity": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "co2_emissions": 27.0,
  "food_type": "beef",
  "quantity": 1.0,
  "unit": "kg CO2e",
  "equivalents": {
    "car_km": 225.0,
    "trees_days": 4500.0
  }
}
```

**Supported Food Types:**
- `beef`, `lamb`, `pork`, `chicken`, `turkey`
- `fish`, `shrimp`
- `cheese`, `milk`, `eggs`
- `vegetables`, `potatoes`, `rice`, `grains`, `beans`, `nuts`

**Error Response:**
```json
{
  "success": false,
  "error": "food_type is required"
}
```

## 🎨 Customization

### Colors & Branding

Edit CSS variables in `static/css/style.css`:

```css
:root {
  --cheval-gul: #ffdc96;
  --cheval-orange: #ffb793;
  --cheval-bla: #d2e1f0;
  --cheval-gron: #d0ebd2;
  --portalThemeColor1: #84d189;
  /* ... more colors */
}
```

### Add New Pages

1. **Create template** in `templates/`:
   ```html
   {% extends "base.html" %}
   {% block title %}Your Page Title{% endblock %}
   {% block content %}
   <!-- Your content here -->
   {% endblock %}
   ```

2. **Add route** in `app.py`:
   ```python
   @app.route('/your-page')
   def your_page():
       return render_template('your_page.html')
   ```

3. **Add to navigation** in `templates/partials/header.html`

### Database Models

To add or modify database models:

1. Edit models in `app.py`
2. For production, use Flask-Migrate:
   ```bash
   pip install Flask-Migrate
   flask db init
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

## 📁 Project Structure

```
powerpages-migration-1/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│       ├── deploy.yml      # Automated deployment
│       └── code-quality.yml # Code quality checks
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── okologi.css
│   │   └── style.css       # Main stylesheet
│   ├── images/             # Image assets
│   └── js/
│       └── main.js         # Main JavaScript
├── templates/
│   ├── base.html           # Base template
│   ├── home.html           # Landing page
│   ├── login.html          # Authentication
│   ├── register.html
│   ├── dashboard.html      # User dashboard
│   ├── admin.html          # Admin panel
│   ├── calculator.html     # CO2 calculator
│   ├── contact.html        # Contact form
│   ├── search_results.html # Search results
│   ├── 404.html            # Error pages
│   ├── 500.html
│   ├── emissions/          # Emissions section
│   ├── okologi/            # Organic food section
│   └── partials/
│       ├── header.html     # Shared header
│       └── footer.html     # Shared footer
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku configuration
├── runtime.txt            # Python version
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

## 🔒 Security

### Production Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Change admin password from default
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS (automatic on Heroku)
- [ ] Use environment variables for sensitive data
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Implement rate limiting (optional)
- [ ] Regular dependency updates
- [ ] Enable Heroku security features

### Reporting Vulnerabilities

Please report security vulnerabilities to the repository maintainer privately.

## 🐛 Troubleshooting

### Database Errors

```bash
# Reset local database
rm vidensbank.db
flask init-db

# On Heroku
heroku pg:reset DATABASE
heroku run flask init-db
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
```

### Heroku Deployment Issues

```bash
# Check logs
heroku logs --tail

# Verify environment variables
heroku config

# Restart app
heroku restart

# Check dyno status
heroku ps
```

### Port Already in Use

```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

## 📊 Monitoring

### Health Check

Monitor your application health at `/health`:

```bash
curl https://your-app.herokuapp.com/health
```

### Logs

```bash
# View real-time logs
heroku logs --tail

# View specific number of lines
heroku logs -n 500

# Filter logs
heroku logs --source app
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for Cheval Blanc Kantiner
- Migrated from Microsoft Power Pages
- Uses Theinhardt and AWConqueror fonts for branding

## � Contact

For questions or support, please open an issue on GitHub or contact the maintainer.

---

**Built with ❤️ for sustainability** 🌱
