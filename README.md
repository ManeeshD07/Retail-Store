Retail Store Monorepo
======================

Full-stack playground for a retail storefront UI powered by a Flask backend and Next.js frontend. The repo is split into two workspaces:

- `backend/` — Flask API with an application factory in `app/__init__.py` and entry point `wsgi.py`.
- `frontend/` — Next.js client bootstrapped with Vite. Shared UI state and components live under `src/app`.

Getting Started
---------------

### Backend

```
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/wsgi.py
```

Environment variables can be provided through a `.env` file in the repo root. See `backend/wsgi.py` for the factory usage.

### Frontend

```
cd frontend
npm install
npm run dev
```

Other useful scripts:

- `npm run build` — generate a production bundle.
- `npm run preview` — serve the built bundle locally.
- `npm run lint` — run ESLint using `eslint.config.mjs`.

Docker Compose
--------------

The provided `docker-compose.yml` spins up MongoDB, the Flask API, the Next.js web server, a seeding job, and a Playwright runner. Bring everything up with:

```
docker compose up --build
```

MongoDB data persists using the named volume `mongo`. Update `.env` values or compose service environment variables to match your deployment configuration.

Testing
-------

- Backend tests: add `pytest` cases under `backend/tests/`.
- Frontend e2e tests: add Playwright specs under `frontend/tests/` and run with `npx playwright test`.

Document manual verification steps in PR descriptions when automated coverage is not yet available.

Contributing
------------

- Follow Conventional Commits (`feat:`, `fix:`, `chore:`) for pull requests.
- Run `npm run lint` before committing frontend changes.
- Store secrets in `.env` (ignored by Git) and expose only the values required by the frontend using the `VITE_` or `NEXT_PUBLIC_` prefixes.
