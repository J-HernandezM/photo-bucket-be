# photo-bucket-be

Photo Bucket is a personal photo storage and management service. It provides an API for uploading, organizing, and retrieving images, along with support for metadata, albums, and efficient media handling. The goal is to offer a self-hosted solution where users can securely manage their own photo library with full control over storage, processing, and access.

## Running Locally with Docker

This project includes a full Dockerized development environment, using `Dockerfile-dev` and `docker-compose.yml` to run both the API and the database.
Hot-reload is supported through the mounted volume in the API service.

### 1. Build and Start the Services

Ensure that the API binds to `0.0.0.0` so it can be accessed from your host machine at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

Basic startup:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

Rebuild and force recreation:

```bash
docker compose up --build --force-recreate
```

### 2. Useful Commands

Follow API logs:

```bash
docker compose logs -f photo-api
```

Open a shell inside the container:

```bash
docker compose exec photo-api sh
```

Run database migrations manually:

```bash
docker compose run --rm photo-api alembic upgrade head
```

---

## Alembic Migrations

Database migrations are managed using **Alembic**.

### Creating a New Migration

```bash
alembic revision --autogenerate -m "your_message_here"
```

Alembic will auto-detect model changes located in the `app.models` package, **as long as all models are imported in `app/models/__init__.py`**.

### Migration Health Checks

- `alembic heads` should return **only one head**
- `alembic branches` should return **no branches**

To apply migrations:

```bash
alembic upgrade head
```
