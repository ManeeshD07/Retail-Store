# Repository Guidelines

## Project Structure & Module Organization
- `backend/` hosts the Flask service; `app/__init__.py` defines the application factory and API routes, while `wsgi.py` is the runnable entry point.
- `frontend/` contains the Vite + React client. Keep shared UI state in `src/` (components in `src/App.jsx`, hooks/utilities alongside feature folders) and static assets in `public/` or `src/assets/`.
- Add automated tests next to the layer they cover (`backend/tests/` for Flask, `frontend/tests/` for Playwright) so runtimes stay isolated.

## Build, Test, and Development Commands
```bash
# Backend setup
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/wsgi.py

# Frontend workflows
cd frontend && npm install
npm run dev      # start Vite with live reload
npm run build    # production bundle to dist/
npm run preview  # serve the built bundle locally
npm run lint     # ESLint pass using eslint.config.js
```

## Coding Style & Naming Conventions
- Python: adhere to PEP 8 with 4-space indents, snake_case modules, and descriptive Blueprint or route names (`products_bp`). Use type hints for new endpoints.
- React: favor functional components in PascalCase (`ProductList`), hooks/utilities in camelCase, and colocate styles (`Component.css`) beside components. Keep imports ordered: React, third-party, then local paths.
- Run `npm run lint` before committing; configure any additional rules in `eslint.config.js`.

## Testing Guidelines
- Frontend end-to-end coverage uses Playwright; place specs under `frontend/tests/` and run `npx playwright test`. Target smoke flows (product listing, auth, cart) whenever UI changes.
- Backend tests should live in `backend/tests/` using `pytest` plus Flask’s test client; add fixtures for Mongo mocks. Aim for meaningful coverage over raw percentages.
- Document any manual test steps in the PR description until automated coverage exists.

## Commit & Pull Request Guidelines
- There is no existing Git history; start using Conventional Commits (`feat:`, `fix:`, `chore:`) with a concise imperative subject and context in the body.
- Each PR should describe the change scope, link relevant issues, note migrations/config updates, and paste `npm run lint` or test results.
- Request review from both frontend and backend owners when touching shared contracts (API schema, DTOs, env variables).

## Environment & Configuration
- Store secrets in a `.env` ignored from Git; read values in Flask via `python-dotenv` and expose only necessary keys to the frontend via Vite env prefixes (`VITE_`).
- Keep development data lightweight—seed endpoints with mock fixtures instead of editing `src/App.jsx` directly.
