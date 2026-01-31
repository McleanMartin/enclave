# Copilot Instructions for Enclave

## Project Overview
**Enclave** is a Django 5.2-based REST API project ("Geoflow Mapper") with Celery task queuing, comprehensive authentication (allauth + MFA), and a custom user model. It's structured as a modular Django application with API-first architecture.

**Key Tech Stack:**
- Django 5.2 with DRF (Django REST Framework)
- PostgreSQL database with Redis caching/message broker
- Celery for async tasks (task queue + beat scheduler)
- drf-spectacular for OpenAPI/Swagger documentation
- pytest-django for testing
- Python 3.13

## Architecture & Major Components

### Core Structure
- **`config/`**: Django configuration (settings by environment, URL routing, WSGI)
  - `settings/base.py`: Shared settings, defines installed apps, middleware, REST framework config
  - `settings/local.py`, `production.py`, `test.py`: Environment-specific overrides
  - `api_router.py`: Central API endpoint registration using DRF's SimpleRouter
  - `urls.py`: Main URL configuration (routes to API router and allauth)
  - `celery_app.py`: Celery initialization and task discovery

- **`enclave/`**: Main application package
  - `users/`: Core user management (models, auth, API)
    - `models.py`: Custom `User` model (extends AbstractUser, uses `name` instead of first/last_name)
    - `api/`: REST API views/serializers with OpenAPI schema
    - `tasks.py`: Celery tasks (e.g., `get_users_count()`)
  - `geoflow/`: Core domain app for GeoFlow features (customers, products, transport activity)
    - `models.py`: `Product`, `Customer`, `TransportActivity` (latitude/longitude stored as decimals; route stored as JSON)
    - `api/`: DRF serializers and ViewSets (`products`, `customers`, `transport-activities` registered in `config/api_router.py`)
    - `tasks.py`: Celery tasks (e.g., `geocode_customer`) that use `enclave.arcgis.services.ArcGISClient` for geocoding
  - `contrib/sites/`: Django sites framework extension
  - `static/`, `templates/`: Frontend assets (Bootstrap 5 + allauth templates)

### Key Design Patterns

**Custom User Model:**
- All auth uses `enclave.users.models.User` (set in `AUTH_USER_MODEL = "users.User"`)
- Simplified to single `name` field instead of first/last names
- Always update `forms.SignupForm` and `SocialSignupForms` when adding user signup fields

**API Architecture:**
- DRF ViewSets + Serializers (e.g., `UserViewSet` in `enclave/users/api/views.py`)
- Endpoint: `/api/users/` (registered via `config/api_router.py`)
- Authentication: Token-based (REST framework authtoken) + allauth backend
- API documentation auto-generated via drf-spectacular: `/api/schema/swagger/`

**Async Tasks (Celery):**
- Message broker: Redis (REDIS_URL setting)
- Result backend: Redis
- Beat scheduler: DatabaseScheduler (periodic tasks configured in Django admin)
- Task time limits: 5 min hard, 1 min soft
- Serialization: JSON only (accept_content, task_serializer, result_serializer)

## Developer Workflows

### Running the Project Locally
```bash
# Install dependencies (via uv or pip)
uv sync

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Start Celery worker (separate terminal)
celery -A config worker -l info

# Start Celery beat scheduler (separate terminal)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Testing
```bash
# Run all tests
pytest

# Run specific app tests
pytest enclave/users/tests/

# Run with coverage
pytest --cov=enclave

# Run API tests with OpenAPI schema validation
pytest enclave/users/tests/api/
```

Test configuration uses `config.settings.test` (see `pyproject.toml`). Tests reuse DB (`--reuse-db`) for speed.

### Code Quality
- **Pre-commit hooks**: Ruff (linting/formatting), mypy (type checking), djLint (template linting)
- **Frontend**: Tailwind is included via CDN in `base.html` for rapid development; for production add a build step and purge CSS.
- **Type checking**: mypy enabled with Django/DRF plugins; migrations excluded
- **Linting**: Ruff configured in `pyproject.toml` (selected checks in ruff section)
- **Formatting**: Applied via pre-commit before commits

### CI/CD
GitHub Actions (`.github/workflows/ci.yml`):
- Pre-commit hook validation
- pytest suite with PostgreSQL 17 + Redis 7.2 services
- Triggered on: PR to `main`, push to `main` (ignores `docs/` changes)

## Critical Conventions & Integration Points

### URL Routing
- API endpoints centralized in `config/api_router.py` using `SimpleRouter.register()`
- Authentication URLs: `allauth` (accounts, MFA, social)
- Admin: `/admin/`
- Static files: `/static/`, Media: `/media/`

### Settings Management
- Environment variables via `django-environ` (`.env` files in `.envs/.local/` or `.envs/.production/`)
- Database: `DATABASE_URL` env var (default: PostgreSQL local database)
- Email backend: Configurable via `EMAIL_BACKEND` (default: console in dev)

### REST Framework Configuration
- Default pagination: Handled by DRF settings
- Schema auto-generation: drf-spectacular (replaces older coreapi)
- CORS: Enabled via `django-cors-headers`, URLs regex in `CORS_URLS_REGEX`
- Authentication: TokenAuthentication + SessionAuthentication

### Migrations & Models
- Custom migrations in `enclave/users/migrations/` and `enclave/contrib/sites/migrations/`
- Always create migrations after model changes: `python manage.py makemigrations`
- Apply: `python manage.py migrate`
- Sites framework: Pre-configured for multi-site support

### File Organization for New Features
1. Model: `enclave/{app}/models.py`
2. Serializer: `enclave/{app}/api/serializers.py`
3. View/ViewSet: `enclave/{app}/api/views.py`
4. Register in: `config/api_router.py`
5. Tests: `enclave/{app}/tests/test_api/` (create if needed) or `test_views.py`
6. Async tasks: `enclave/{app}/tasks.py` (decorate with `@shared_task()`)

### Template Conventions
- Base template: `enclave/templates/base.html` (Bootstrap 5)
- Allauth customizations: `enclave/templates/allauth/` (layouts + elements)
- Use crispy forms: `{% load crispy_forms_tags %}` + `|crispy` filter

## Common Tasks for AI Agents

**Adding a new API endpoint:**
1. Create serializer in `api/serializers.py`
2. Add ViewSet method/action in `api/views.py`
3. Register in `config/api_router.py`: `router.register(r'endpoint', ViewSet)`
4. Write tests in `tests/api/test_views.py`

**Adding a Celery task:**
1. Define in `enclave/{app}/tasks.py` with `@shared_task()` decorator
2. Optionally register periodic task in Django admin (Periodic Tasks)
3. Test with `pytest` (task execution tested synchronously in test settings)

**Testing tasks that call ArcGIS:**
 - Tests should mock `enclave.arcgis.services.ArcGISClient` to avoid requiring the ArcGIS SDK or external network calls. See `enclave/geoflow/tests/test_tasks.py` for an example using `monkeypatch`.

**Adding user fields:**
1. Update `User` model in `enclave/users/models.py`
2. Update `SignupForm` in `enclave/users/forms.py`
3. Update serializer in `enclave/users/api/serializers.py`
4. Create migration: `python manage.py makemigrations users`
5. Add to `UserSerializer` for API exposure

**Running database commands:**
- Shell: `python manage.py shell`
- Migrations: `python manage.py makemigrations` → `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`

## Documentation & Resources
- Django settings: `config/settings/base.py` (comprehensive comments)
- API docs (auto-generated): `http://localhost:8000/api/schema/swagger/`
- CI config: `.github/workflows/ci.yml`
- Project metadata: `pyproject.toml` (dependencies, tool configs)
 - Project summary: `docs/project_summary.md`

