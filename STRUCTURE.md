# Vidensbank Directory Structure

```
vidensbank/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for Heroku
├── Procfile                        # Heroku process file
├── .gitignore                      # Git ignore rules
├── vidensbank.db                   # SQLite database
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css       # Bootstrap framework
│   │   └── style.css               # Custom styles
│   ├── js/
│   │   └── main.js                 # JavaScript functions
│   └── images/                     # All images
└── templates/
    ├── base.html                   # Base template with navigation
    ├── home.html                   # Homepage
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    ├── contact.html                # Contact form
    ├── climate_potential.html      # Climate calculator
    ├── dashboard.html              # User dashboard
    ├── admin.html                  # Admin panel
    ├── search_results.html         # Search results
    ├── 404.html                    # 404 error page
    ├── 500.html                    # 500 error page
    ├── partials/
    │   ├── header.html             # Navigation header
    │   └── footer.html             # Footer
    ├── emissions/
    │   ├── main.html               # Emissions overview
    │   ├── food_emissions.html     # Food emissions details
    │   ├── climate_data.html       # Climate data & trends
    │   ├── market_analysis.html    # Market analysis
    │   ├── data_driven_approach.html # Data-driven approach
    │   └── political_landscape.html  # Political landscape
    └── ecology/
        └── main.html               # Organic agriculture info
```

## Routes

- `/` - Homepage
- `/emissioner-og-baeredygtighed` - Emissions main page
- `/emissioner-og-baeredygtighed/fodevare-relaterede-emissioner` - Food emissions
- `/emissioner-og-baeredygtighed/klimadata` - Climate data
- `/emissioner-og-baeredygtighed/branchepraestation` - Market analysis
- `/emissioner-og-baeredygtighed/datadrevet-tilgang` - Data-driven approach
- `/emissioner-og-baeredygtighed/politisk-landskab` - Political landscape
- `/oekologi` - Ecology/organic agriculture
- `/klimapotentiale` - Climate potential calculator
- `/contact` - Contact form
- `/login` - Login
- `/register` - Register
- `/dashboard` - User dashboard (protected)
- `/admin` - Admin panel (protected)

## Heroku Deployment

The application is ready for Heroku deployment with:
- **Procfile**: Configured to run with gunicorn
- **requirements.txt**: All Python dependencies listed
- **runtime.txt**: Python 3.12.0 specified
- **PostgreSQL support**: Automatic database URL conversion for Heroku Postgres
