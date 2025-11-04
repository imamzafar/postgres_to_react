# Full-Stack Inventory Demo (FastAPI - PostgreSQL - React)

This project delivers an end-to-end CRUD example using PostgreSQL for data storage, FastAPI for the backend REST service, and a Vite-powered React frontend. Everything is designed to run locally first, with guidance for deploying to Azure when you are ready.

## Project Structure

```
postgres_to_react/
|-- backend/              # FastAPI application and database scripts
|   |-- app/              # FastAPI app, SQLAlchemy models, schemas, CRUD logic
|   |-- scripts/          # Helper scripts (database bootstrap, etc.)
|   |-- requirements.txt  # Python dependencies
|   `-- .env.example      # Sample backend environment variables
|-- notebooks/            # Jupyter notebooks for direct PostgreSQL interaction
|-- frontend/             # React (Vite) single page application
|   |-- src/              # React components, API client, styles
|   |-- package.json      # Node dependencies and scripts
|   `-- .env.example      # Sample frontend environment variables
`-- README.md             # Documentation
```

## Backend Overview

- Framework: FastAPI
- Database layer: SQLAlchemy 2.x (synchronous engine)
- Database: PostgreSQL (local instance)
- CRUD endpoints:
  - `GET /items` - list items
  - `POST /items` - create item
  - `GET /items/{id}` - read item
  - `PUT /items/{id}` - update item
  - `DELETE /items/{id}` - delete item
- Extras:
  - `GET /health` for a quick service check
  - Automatic table creation on startup
  - Database bootstrap script `backend/scripts/create_database.py`
  - CORS allows React dev servers on `http://localhost:5173` and `http://localhost:3000`

## Frontend Overview

- React 18 with Vite for fast development
- Axios API client with configurable base URL
- Item form supports both create and update flows
- Item list with edit and delete actions
- Loading and error states included
- Basic responsive styling with modern CSS

## Prerequisites

- Python 3.10 or newer (3.11 recommended)
- Node.js 18 or newer (npm or pnpm available on PATH)
- PostgreSQL 13 or newer running locally
- Ability to create databases using your PostgreSQL user

## 1. Local Backend Setup

1. Open a terminal and activate the project folder.
2. Create and activate a virtual environment (recommended):
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # Windows PowerShell
   # source .venv/bin/activate    # macOS/Linux
   ```
3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure backend environment variables:
   ```powershell
   Copy-Item .env.example .env
   ```
   Edit `.env` to match your local PostgreSQL credentials. Minimum value:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventory_db
   ```
5. Create the PostgreSQL database (runs safely if it already exists):
   ```powershell
   python scripts/create_database.py
   ```
6. Start the FastAPI server:
   ```powershell
   uvicorn app.main:app --reload
   ```
   The API is available at `http://127.0.0.1:8000` with interactive docs at `/docs`.

## 2. Local Frontend Setup

1. Open a new terminal window or tab:
   ```powershell
   cd frontend
   npm install
   ```
2. Configure frontend environment variables:
   ```powershell
   Copy-Item .env.example .env
   ```
   Confirm `VITE_API_BASE_URL` matches the backend URL (default `http://localhost:8000`).
3. Start the Vite dev server:
   ```powershell
   npm run dev
   ```
4. Open `http://localhost:5173` in your browser to use the app.

Keep both servers running during development for full-stack hot reloading.

## CRUD Quick Test

1. Use the React form to create a new inventory item.
2. Update the item to confirm edit functionality.
3. Delete the item and verify it disappears from the table.
4. Optionally call the API directly through `http://127.0.0.1:8000/docs`.

You can validate the database contents with `psql` or another client:
```sql
SELECT id, name, quantity, price, updated_at FROM items ORDER BY updated_at DESC;
```

## Working Directly With PostgreSQL

Although the FastAPI app automatically creates the `items` table for you, it is often helpful to interact with PostgreSQL manually—either to inspect the schema, seed the database, or troubleshoot connectivity.

### Jupyter Notebook Workflow

The `notebooks/postgres_interaction.ipynb` notebook walks through connecting to PostgreSQL, creating the `items` table, inserting sample rows, and querying the results.

1. **Install Jupyter (if needed)** inside your Python environment:
   ```powershell
   pip install notebook
   ```
   The notebook also relies on packages already listed in `backend/requirements.txt` plus `pandas` for DataFrame output (optional).
2. **Launch Jupyter** from the project root or the `notebooks` folder:
   ```powershell
   jupyter notebook
   ```
3. Open `notebooks/postgres_interaction.ipynb` and run the cells sequentially. The notebook will load environment variables from `backend/.env`, connect using SQLAlchemy, create tables, insert data, and display query results.

### 1. Connect with `psql`

```powershell
psql "postgresql://postgres:postgres@localhost:5432/inventory_db"
```

Replace the username, password, host, port, and database name with values that match your environment. If you prefer using separate prompts, you can omit the password and enter it interactively:

```powershell
psql -h localhost -p 5432 -U postgres -d inventory_db
```

### 2. Create Tables Manually (Optional)

FastAPI’s SQLAlchemy models will create the schema, but you can mirror the same table definition with raw SQL if needed:

```sql
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_items_name ON items (name);
```

### 3. Load Sample Data

```sql
INSERT INTO items (name, description, quantity, price)
VALUES
    ('MacBook Pro', '16-inch laptop', 4, 2399.00),
    ('Dell Ultrasharp Monitor', '27-inch 4K display', 10, 449.99),
    ('Logitech MX Master 3', 'Wireless mouse', 25, 99.99);
```

### 4. Test the Connection Programmatically

You can run a quick Python script in the backend virtual environment to validate connectivity outside of FastAPI:

```python
import sqlalchemy as sa

engine = sa.create_engine("postgresql://postgres:postgres@localhost:5432/inventory_db")

with engine.connect() as conn:
    result = conn.execute(sa.text("SELECT COUNT(*) FROM items"))
    print("Items in inventory:", result.scalar())
```

Or use the `psycopg2` driver directly:

```python
import psycopg2

conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/inventory_db")
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, name FROM items LIMIT 5;")
    for row in cur.fetchall():
        print(row)
```

These snippets are useful when you want to verify credentials, ensure network access, or pre-load data before starting the FastAPI server.

## Suggested Local Validation

- Backend: use FastAPI docs or curl to hit each endpoint.
- Frontend: ensure the form and table reflect changes instantly.
- Integration: insert or update a record via the API, then check the UI (and vice versa).

## Azure Deployment Guide (High Level)

Plan for the following when moving to Azure:

1. **PostgreSQL**
   - Provision Azure Database for PostgreSQL (Flexible Server or Single Server).
   - Create the target database (`inventory_db`).
   - Configure firewall or VNet rules and store credentials securely.

2. **FastAPI Backend**
   - Containerize with a Dockerfile similar to:
     ```dockerfile
     FROM python:3.11-slim
     WORKDIR /app
     COPY backend/requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY backend/app ./app
     ENV PYTHONPATH=/app
     CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
     ```
   - Push the image to Azure Container Registry.
   - Deploy to Azure App Service for Containers or Azure Container Apps.
   - Set `DATABASE_URL` (and other secrets) via App Service settings or Azure Key Vault.

3. **React Frontend**
   - Build locally: `npm run build` (outputs `frontend/dist`).
   - Deploy using Azure Static Web Apps or Azure Storage + CDN.
   - During build, configure `VITE_API_BASE_URL` to point to the Azure backend.
   - Configure CORS on the backend to allow the chosen frontend domain.

4. **Operations**
   - Enable HTTPS on all endpoints.
   - Monitor with Azure Monitor or Application Insights.
   - Configure automated backups (Azure PostgreSQL handles this by default).
   - Set up CI/CD (GitHub Actions or Azure DevOps) to automate deploys.

## Troubleshooting Checklist

- psycopg2 installation issues: install PostgreSQL client libraries (`libpq`) or rely on the bundled binary wheel.
- Port conflicts: adjust FastAPI (`--port 9000`) or Vite (`npm run dev -- --port 3000`) and update `.env` files.
- CORS errors: ensure allowed origins in `backend/app/main.py` match your frontend URL.
- npm not found: install Node.js from https://nodejs.org before running frontend commands.
- Database login errors: confirm PostgreSQL is accepting TCP connections and credentials are correct.

## Next Ideas

- Add pytest-based API tests with FastAPI TestClient.
- Expand the data model (categories, suppliers, audit trail).
- Add authentication and authorization.
- Create Docker Compose files for consistent local and cloud environments.

With these pieces in place, you can run the entire stack locally today and smoothly transition to Azure when needed. Happy building!
