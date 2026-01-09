# RankSoccerCSOC

RankSoccerCSOC is a full-stack application designed for soccer ranking and competition management. It features a Django backend with Celery task processing and a Vue 3 frontend with Tailwind CSS 4.

## Core Features
- **Modern Backend**: Django 4.2 + DRF for robust API development.
- **Reactive Frontend**: Vue 3 (Composition API) with Vite.
- **Task Orchestration**: Celery + Redis for asynchronous background jobs.
- **Containerized Architecture**: Docker-based environment for seamless development and deployment.
- **Enhanced Admin**: Modernized dashboard using `django-jazzmin`.

## Project Structure
- `Backend/`: Django source code, settings, and requirements.
- `Frontend/`: Vue 3 source code, components, and package configuration.
- `docs/`: Comprehensive project documentation.
- `docker-compose.prod.yml`: Production services orchestration.
- `docker-compose.db.yml`: Infrastructure services (PostgreSQL, Redis).

## Documentation
Detailed documentation is available in the `docs/` directory:
- [Project Overview & PDR](docs/project-overview-pdr.md)
- [Codebase Summary](docs/codebase-summary.md)
- [Code Standards](docs/code-standards.md)
- [System Architecture](docs/system-architecture.md)

## Quick Start (Docker)

1. **Prerequisites**: Ensure you have Docker and Docker Compose installed.
2. **Environment**: Create a `.env` file based on the project requirements.
3. **Start Infrastructure**:
   ```bash
   docker-compose -f docker-compose.db.yml up -d
   ```
4. **Start Application**:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

## Development Workflow
- **Backend**: Standard Django management commands (`migrate`, `runserver`).
- **Frontend**: Vite development server (`npm run dev`).
- **Tests**: Follow the guidelines in [Code Standards](docs/code-standards.md).

## Technology Stack
- **Backend**: Python 3.12, Django 4.2.0, DRF, Celery, PostgreSQL, Redis.
- **Frontend**: Vue 3, Vite, Tailwind CSS 4, Axios, Pinia, Vue Router.
- **Deployment**: Gunicorn, Whitenoise, Docker.
