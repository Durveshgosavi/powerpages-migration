# Contributing to Vidensbank

Thank you for considering contributing to Vidensbank! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Include:**
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. **Search existing feature requests**
2. **Create a detailed proposal** including:
   - Use case and benefits
   - Proposed implementation
   - Potential drawbacks
   - Alternative solutions considered

### Pull Requests

#### Before Submitting

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Test your changes thoroughly**
4. **Update documentation** if needed
5. **Follow code style guidelines**

#### PR Guidelines

- **One feature per PR** - Keep changes focused
- **Write clear commit messages**
- **Include tests** for new features
- **Update README** if adding new functionality
- **Reference related issues**

#### Commit Message Format

```
type(scope): brief description

Detailed explanation of changes (if needed)

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(calculator): add new emission factors for dairy products

Added comprehensive emission factors for various dairy products
including milk, cheese, and yogurt based on latest research.

Fixes #45
```

```
fix(auth): prevent duplicate email registrations

Added email validation check before user registration to prevent
duplicate accounts with the same email address.

Fixes #78
```

## Development Setup

### Prerequisites

- Python 3.12+
- Git
- Virtual environment tool

### Setup Steps

1. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/powerpages-migration.git
   cd powerpages-migration
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database:**
   ```bash
   flask init-db
   ```

6. **Run tests:**
   ```bash
   pytest
   ```

7. **Start development server:**
   ```bash
   python app.py
   ```

## Code Style

### Python

Follow PEP 8 style guide:

```bash
# Install tools
pip install black flake8 isort

# Format code
black .

# Check style
flake8 .

# Sort imports
isort .
```

**Guidelines:**
- Max line length: 127 characters
- Use descriptive variable names
- Add docstrings to functions and classes
- Type hints are encouraged

### HTML/CSS

- Use semantic HTML5 elements
- Follow existing naming conventions
- Keep CSS organized by sections
- Use CSS custom properties for colors

### JavaScript

- Use ES6+ features
- Follow existing code structure
- Add comments for complex logic
- Test in multiple browsers

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_calculator.py

# Run specific test
pytest tests/test_calculator.py::test_co2_calculation
```

### Writing Tests

```python
def test_feature_name():
    """Test description"""
    # Arrange
    input_data = {...}
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Test both success and failure paths

## Documentation

### Code Documentation

```python
def calculate_emissions(food_type: str, quantity: float) -> dict:
    """
    Calculate CO2 emissions for a given food type and quantity.
    
    Args:
        food_type (str): Type of food (e.g., 'beef', 'chicken')
        quantity (float): Quantity in kilograms
        
    Returns:
        dict: Dictionary containing emission data with keys:
            - co2_emissions: Total emissions in kg CO2e
            - equivalents: Contextual equivalents
            
    Raises:
        ValueError: If quantity is negative or food_type is invalid
        
    Example:
        >>> calculate_emissions('beef', 1.0)
        {'co2_emissions': 27.0, 'equivalents': {...}}
    """
    # Implementation
```

### README Updates

- Keep README.md current with features
- Update API documentation when endpoints change
- Add examples for new features
- Update troubleshooting section as needed

## Project Structure

```
powerpages-migration-1/
├── app.py                 # Main application - core routes and config
├── models.py              # Database models (if separated)
├── forms.py               # Form definitions (if using Flask-WTF)
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Image assets
├── templates/            # Jinja2 templates
├── tests/                # Test suite
├── docs/                 # Additional documentation
└── requirements.txt      # Python dependencies
```

## Best Practices

### Security

- Never commit sensitive data (keys, passwords)
- Use environment variables for configuration
- Validate and sanitize all user input
- Use parameterized queries (SQLAlchemy ORM does this)
- Implement proper error handling

### Performance

- Minimize database queries
- Use pagination for large datasets
- Optimize images before committing
- Cache static assets
- Profile before optimizing

### Accessibility

- Use semantic HTML
- Include alt text for images
- Ensure keyboard navigation works
- Maintain sufficient color contrast
- Test with screen readers

### Database

- Use migrations for schema changes
- Never modify production database directly
- Test migrations on staging first
- Keep backup before major changes

## Review Process

1. **Automated checks** run on PR submission
2. **Code review** by maintainers
3. **Testing** in staging environment
4. **Approval** and merge to main branch
5. **Deployment** to production (automated)

## Questions?

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing to Vidensbank!** 🌱
