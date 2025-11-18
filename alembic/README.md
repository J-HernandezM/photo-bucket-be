# Alembic Migrations Guide

## How Migrations Are Configured

- **Database URL**: The database connection string is set via the `DATABASE_URL` environment variable. For local development, this is loaded from a `.env` file using `python-dotenv` in `alembic/env.py`. In production, set `DATABASE_URL` in your environment (CI/CD, ECS, etc).
- **Model Discovery**: All SQLAlchemy models are imported in `app/models/__init__.py` and this module is imported in `alembic/env.py` to ensure Alembic sees all tables for autogenerate.
- **Target Metadata**: Alembic uses `Base.metadata` from `app/db.py` for schema autogeneration.
- **Migration File Naming**: By default, Alembic uses a hash-based revision ID. You can customize the filename pattern in `alembic.ini` with the `file_template` option.

## How to Create a Migration

1. **Edit or add your SQLAlchemy models in `app/models/`.**
2. **Import your new model module in `alembic/env.py`** (e.g., `from app.models import photo`). This ensures Alembic can detect your model for autogenerate.
2. **Generate a migration:**
   ```sh
   alembic revision --autogenerate -m "Describe your change"
   ```
3. **(Optional) Rename the migration file** in `alembic/versions/` to use a sequential prefix (e.g., `01_...`, `02_...`).
4. **Review and edit the generated migration** if needed.

## How to Apply Migrations

```sh
alembic upgrade head
```

## Environment Setup

- For local development, create a `.env` file in the project root with:
  ```
  DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
  ```
- For production, set the `DATABASE_URL` environment variable in your deployment environment.

## Troubleshooting

- If autogenerate produces empty migrations, ensure all models are imported in `app/models/__init__.py` and that `alembic/env.py` imports this module before setting `target_metadata`.
- If you see errors about missing libraries (e.g., `libpq`), install the required system packages (e.g., `libpq-dev` on Ubuntu).

---

For more details, see the [Alembic documentation](https://alembic.sqlalchemy.org/).
