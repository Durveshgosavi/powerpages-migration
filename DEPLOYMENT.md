# ============================================================================
# DEPLOYMENT GUIDE - Vidensbank Flask Application
# ============================================================================

## Prerequisites

Before deploying, ensure you have:

1. ✅ Heroku account (free tier available)
2. ✅ Heroku CLI installed
3. ✅ Git repository initialized
4. ✅ PostgreSQL addon configured
5. ✅ Environment variables set

## Pre-Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` in production
- [ ] Set `FLASK_ENV=production`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Change admin password from default
- [ ] Review and update security headers
- [ ] Ensure HTTPS is enforced

### Configuration
- [ ] Set all required environment variables
- [ ] Configure database URL
- [ ] Set admin email for notifications
- [ ] Configure CORS if needed
- [ ] Set proper log levels

### Database
- [ ] Test database initialization script
- [ ] Plan for data migration (if applicable)
- [ ] Backup existing data
- [ ] Test rollback procedures

### Testing
- [ ] Run all tests locally
- [ ] Test on staging environment
- [ ] Verify all routes work
- [ ] Test authentication flows
- [ ] Verify CO2 calculator API
- [ ] Check responsive design

### Performance
- [ ] Optimize images (compress, resize)
- [ ] Minify CSS/JS (if not done)
- [ ] Enable caching headers
- [ ] Test page load times
- [ ] Configure CDN (optional)

## Deployment Steps

### Step 1: Local Testing

```bash
# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set test environment variables
export SECRET_KEY="test-key"
export FLASK_ENV=development

# Initialize database
flask init-db

# Run application
python app.py

# Test all major features
# - Registration/Login
# - CO2 Calculator
# - Search functionality
# - Contact form
# - Admin panel
```

### Step 2: Heroku Setup

```bash
# Login to Heroku
heroku login

# Create new app (or use existing)
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
heroku config:set FLASK_ENV=production
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set APP_NAME="Vidensbank"

# Verify configuration
heroku config
```

### Step 3: Deploy Application

```bash
# Ensure you're on the correct branch
git branch

# Add all changes
git add .

# Commit changes
git commit -m "Prepare for production deployment"

# Deploy to Heroku
git push heroku main

# Or if using GitHub integration:
# - Go to Heroku Dashboard → Deploy
# - Connect GitHub repository
# - Enable automatic deploys
# - Click "Deploy Branch"
```

### Step 4: Initialize Database

```bash
# Run database initialization
heroku run flask init-db

# Create admin user
heroku run flask create-admin

# Verify database
heroku pg:info
```

### Step 5: Verification

```bash
# Check app status
heroku ps

# View logs
heroku logs --tail

# Test health endpoint
curl https://your-app-name.herokuapp.com/health

# Open application
heroku open
```

## Post-Deployment

### Monitoring

1. **Set up log monitoring:**
   ```bash
   heroku logs --tail
   ```

2. **Enable Papertrail (log management):**
   ```bash
   heroku addons:create papertrail
   ```

3. **Monitor dyno metrics:**
   ```bash
   heroku metrics
   ```

### Scaling

```bash
# Scale web dynos
heroku ps:scale web=1

# For higher traffic:
heroku ps:scale web=2
```

### Maintenance

```bash
# Enable maintenance mode
heroku maintenance:on

# Perform updates/migrations
heroku run flask db upgrade

# Disable maintenance mode
heroku maintenance:off
```

## Troubleshooting

### Application Won't Start

1. Check logs:
   ```bash
   heroku logs --tail
   ```

2. Verify Procfile:
   ```bash
   cat Procfile
   # Should contain: web: gunicorn app:app
   ```

3. Check runtime:
   ```bash
   cat runtime.txt
   # Should contain: python-3.12.0
   ```

### Database Errors

1. Reset database:
   ```bash
   heroku pg:reset DATABASE
   heroku run flask init-db
   ```

2. Check connection:
   ```bash
   heroku pg:info
   heroku pg:psql
   ```

### 503 Service Unavailable

1. Check dyno status:
   ```bash
   heroku ps
   ```

2. Restart dynos:
   ```bash
   heroku restart
   ```

3. Scale up:
   ```bash
   heroku ps:scale web=1
   ```

### Environment Variable Issues

```bash
# List all config vars
heroku config

# Set missing variables
heroku config:set KEY=VALUE

# Unset variables
heroku config:unset KEY
```

## Rollback Procedure

If deployment fails:

```bash
# View releases
heroku releases

# Rollback to previous version
heroku rollback v<version-number>

# Example:
heroku rollback v23
```

## GitHub Actions CI/CD

### Setup Secrets

1. Go to GitHub repository → Settings → Secrets
2. Add these secrets:
   - `HEROKU_API_KEY`: Get from Heroku account settings
   - `HEROKU_APP_NAME`: Your app name
   - `HEROKU_EMAIL`: Your Heroku email

### Workflow

The deployment workflow:
1. Runs on push to main branch
2. Executes tests
3. Checks code quality
4. Deploys to Heroku
5. Runs health checks
6. Notifies on failure

### Manual Trigger

```bash
# Trigger workflow manually
# Go to GitHub → Actions → Deploy to Heroku → Run workflow
```

## Custom Domain (Optional)

```bash
# Add custom domain
heroku domains:add www.yourdomain.com

# Get DNS target
heroku domains

# Configure DNS:
# Add CNAME record pointing to Heroku DNS target
```

## SSL Certificate

Heroku provides automatic SSL:
- Included in all paid dynos
- Automatic renewal
- No configuration needed

## Backup Strategy

### Database Backups

```bash
# Create manual backup
heroku pg:backups:capture

# Schedule automatic backups (paid dynos)
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/New_York'

# List backups
heroku pg:backups

# Download backup
heroku pg:backups:download
```

### Code Backups

- Use Git tags for releases
- Maintain separate production branch
- Document all changes

## Performance Optimization

### Enable Caching

Add Flask-Caching for better performance:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Use CDN

Configure CloudFlare or similar CDN for static assets.

### Database Optimization

```bash
# Analyze database performance
heroku pg:diagnose

# Run vacuum (cleanup)
heroku pg:psql -c "VACUUM ANALYZE;"
```

## Security Best Practices

1. **Regular Updates:**
   ```bash
   pip list --outdated
   pip install -r requirements.txt --upgrade
   ```

2. **Security Scanning:**
   ```bash
   pip install safety
   safety check
   ```

3. **Monitor Access Logs:**
   ```bash
   heroku logs --source app | grep "POST /login"
   ```

4. **Enable 2FA on Heroku account**

5. **Rotate secrets regularly**

## Support & Resources

- **Heroku Dev Center:** https://devcenter.heroku.com/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **GitHub Issues:** [Your repository]/issues
- **Heroku Status:** https://status.heroku.com/

## Maintenance Schedule

- **Daily:** Monitor logs and health checks
- **Weekly:** Review error reports, check performance metrics
- **Monthly:** Security updates, dependency updates, backup verification
- **Quarterly:** Full security audit, performance optimization review

---

**Last Updated:** 2025-11-13
**Version:** 1.0.0
