# FastAPI Production Boilerplate

A production-grade FastAPI boilerplate with best practices, authentication, database integration, and comprehensive testing setup.

## Features

- ✅ **FastAPI** with async/await support
- ✅ **SQLAlchemy** async database integration
- ✅ **JWT Authentication** with access and refresh tokens
- ✅ **Alembic** database migrations
- ✅ **Pydantic** for data validation
- ✅ **CORS** and security middleware
- ✅ **Structured logging** with file rotation
- ✅ **Error handling** with custom exceptions
- ✅ **Health check** endpoints
- ✅ **Docker** and Docker Compose support
- ✅ **Pytest** testing framework
- ✅ **Environment-based configuration**
- ✅ **Type hints** throughout

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── router.py       # API router
│   │       ├── endpoints/      # API endpoints
│   │       └── schemas/        # Pydantic schemas
│   ├── core/
│   │   ├── config.py           # Configuration management
│   │   ├── security.py         # Authentication utilities
│   │   ├── logging.py          # Logging configuration
│   │   └── exceptions.py       # Custom exceptions
│   └── db/
│       ├── database.py         # Database connection
│       └── models/             # SQLAlchemy models
├── alembic/                    # Database migrations
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
└── .env.example                # Environment variables template
```

## Quick Start

### 1. Clone and Setup

```bash
# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
# Make sure to set SECRET_KEY and DATABASE_URL
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Docker Compose
docker-compose up --build
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Checks
- `GET /api/v1/health/` - Health check
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/` - List users (paginated)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PATCH /api/v1/users/me` - Update current user

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `SECRET_KEY` - Secret key for JWT tokens (required)
- `DATABASE_URL` - PostgreSQL database URL (required)
- `ENVIRONMENT` - Environment (development/production)
- `CORS_ORIGINS` - Allowed CORS origins
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Development

### Code Formatting

```bash
# Format code with black
black app tests

# Sort imports
isort app tests

# Type checking
mypy app
```

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Use a strong `SECRET_KEY`
3. Configure proper `CORS_ORIGINS`
4. Set up proper database backups
5. Use a production WSGI server (e.g., Gunicorn with Uvicorn workers)
6. Set up reverse proxy (Nginx)
7. Enable HTTPS
8. Configure monitoring and logging

## License

MIT
