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

## Environment Variables

Set these in a `.env` file at the project root (use `.env.example` as a template). docker-compose automatically loads `.env`.

- PG_USER: Postgres username used to initialize the DB container.
- PG_PASSWORD: Postgres password used to initialize the DB container.
- PG_DBNAME: Database name created in the DB container.
- DATABASE_URL: Async SQLAlchemy URL for running the app on the host (outside Docker); use `postgresql+asyncpg` and host `localhost`.
- CONTAINER_DATABASE_URL: Async SQLAlchemy URL used by the API container; host should be the compose service name `bucketdb`.
- AWS_ENDPOINT_URL: LocalStack endpoint for host processes (leave empty in prod so AWS is used).
- CONTAINER_AWS_ENDPOINT_URL: LocalStack endpoint from inside containers; use `http://localstack:4566` (service name).
- AWS_REGION: AWS region to target (e.g., `us-east-1`).
- AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY: Required by boto in LocalStack dev (use `test`/`test`); in AWS (ECS), omit and rely on the task role.
- BUCKET_NAME: The S3 bucket where photos are going to be stored.

Note: docker-compose already maps the API’s `DATABASE_URL` from `CONTAINER_DATABASE_URL`. For LocalStack inside the container, map `AWS_ENDPOINT_URL` to `CONTAINER_AWS_ENDPOINT_URL` in the service environment if needed.

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

## LocalStack Setup

LocalStack provides a local AWS cloud environment for development and testing. This project uses it to simulate S3 storage locally.

### Prerequisites

Install the `awslocal` CLI wrapper:

```bash
pip install awscli-local
```

### Deploy Infrastructure

Deploy the CloudFormation stack (creates S3 bucket) to LocalStack:

```bash
./deploy.sh -e dev
```

Use `-e prod` for production environment configuration.

### Interacting with LocalStack S3

List all buckets:

```bash
awslocal s3 ls
```

Upload a file:

```bash
awslocal s3 cp ./path/to/file.jpg s3://photo-bucket-dev/uploads/file.jpg
```

List objects in a bucket:

```bash
awslocal s3 ls s3://photo-bucket-dev --recursive
```

Download a file:

```bash
awslocal s3 cp s3://photo-bucket-dev/uploads/file.jpg ./downloaded.jpg
```

### Volume Persistence

LocalStack uses a named volume (`localstack_data`) to persist state across container restarts. To reset LocalStack completely:

```bash
docker compose down
docker volume rm photo-bucket-be_localstack_data
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
