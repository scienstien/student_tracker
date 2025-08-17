# Student Tracker: Production-Ready Deployment

## Quick Start (Docker Compose)

1. Copy `.env.example` to `.env` and fill out secrets.
2. Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```
3. Run initial migrations and create superuser:
   ```sh
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```
4. Access app at `http://localhost:8000`

## Advanced Features

See `docs/PRODUCTION_READINESS_GUIDE.md` for all advanced features and best practices.

## CI/CD

GitHub Actions workflow is included at `.github/workflows/deploy.yml`.

## Production Notes

- Uses Gunicorn and PostgreSQL out of the box.
- Environment variables control production secrets.
- Static files served via Django collectstatic.