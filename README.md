# AI‑Powered Accessibility Compliance

> **Status:** 🚧 MVP in development – 7‑day sprint

This repository contains a proof‑of‑concept micro‑SaaS that helps website owners audit and improve the accessibility of their pages. It combines a Python/FastAPI backend for running accessibility audits and a Next.js + Tailwind frontend for interacting with the service. Supabase handles authentication, persistence and storage, while Stripe provides subscription billing.

## Architecture

```
┌───────────────┐      POST /scan        ┌──────────────────┐
│ Next.js Front │ ─────────────────────► │ FastAPI Backend  │
│   (Vercel)    │       JSON API         │   (Docker)       │
└───────────────┘ ◄───────────────────── └──────────────────┘
        ▲                GET /scan/{id}          ▲
        │                                         │
        │                                         │
        │                                         │
        │                                         │
┌───────────────┐       Supabase (DB, Auth, Storage)        ┌───────────┐
│ Stripe Billing│  ◄───────────────▲───────────────────────► │ cron jobs │
└───────────────┘                   │                       └───────────┘
                                   │
                         nightly backups & metrics
```

### Backend (`backend/`)

The backend is a FastAPI application that exposes two endpoints:

- `POST /scan` – Accepts a JSON body with a `url` field and queues a new accessibility audit. A new row is inserted into the `scans` table with status `pending`, after which an asynchronous background task invokes headless Chrome/axe‑core (stubbed) to produce a JSON report. The report is stored on disk (or in Supabase storage in production) and the scan record is updated to `completed`.
- `GET /scan/{id}` – Returns the persisted scan, including its status and any associated report metadata.

Data is stored in a simple SQLite database via SQLAlchemy. Sensitive keys (e.g. Supabase service key, Stripe webhook secret) should be encrypted with AES‑256‑GCM using `backend/app/crypto.py`. Tests live under `backend/app/tests/` and can be run with `pytest`.

The application is containerised via a Dockerfile. When deploying to production you should replace the SQLite database with Supabase Postgres and configure the container to access a headless Chrome binary (e.g. using Playwright or Pa11y).

### Frontend (`frontend/`)

The frontend is a Next.js application styled with Tailwind. It exposes a simple landing page (`/`) where users can submit a URL to audit. The form calls the backend API via rewrites configured in `next.config.js`. Results are not yet displayed in the UI; once Supabase authentication and storage are connected, the dashboard can surface completed reports and key SaaS metrics (ARR, MRR, churn).

The project is set up with TypeScript and includes PostCSS/Tailwind configuration. A placeholder Stripe webhook endpoint is defined in `src/pages/api/stripe/webhook.ts`; you will need to verify signatures and update Supabase subscription records on real events.

### Supabase

To run this project end‑to‑end you will need a free Supabase project. Create tables named `users`, `scans` and `subscriptions`, and a storage bucket called `reports`. Generate a service role API key and encrypt it using the helper in `backend/app/crypto.py`. Supabase Auth (magic‑link) can be enabled to provide user sign‑ups via the frontend.

Nightly backups can be configured by scheduling a `pg_dump` to the `reports` bucket using Supabase’s built‑in backup functionality or via GitHub Actions.

### Stripe

Stripe Billing and Stripe Tax can be enabled with plans of $49/$99/$199 USD per month. Configure a webhook endpoint at `/api/stripe/webhook` and set the signing secret as an environment variable (`STRIPE_WEBHOOK_SECRET`). The webhook handler should activate or deactivate subscriptions in the `subscriptions` table.

### CI/CD

GitHub Actions definitions in `.github/workflows/` provide basic pipelines:

- **backend.yml** – installs dependencies, runs tests with pytest and builds a Docker image.
- **frontend.yml** – installs Node.js dependencies and builds the Next.js app.
- **cron_seo.yml** – scheduled job that generates a placeholder SEO blog post every two days. Replace the placeholder script with an actual call to an LLM (e.g. OpenAI) and commit the result to the repository or your CMS.

### Local development

1. Install Python 3.10 and Node.js 20.
2. In one terminal, start the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. In another terminal, start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. Visit `http://localhost:3000` and submit a URL to kick off a scan.

### Deployment

The recommended stack uses Vercel’s Hobby plan for the frontend and Supabase’s free tier for the backend database and storage. The FastAPI backend can be deployed on a lightweight container host such as Fly.io or Render on their free tier. Ensure environment variables are set for:

- `NEXT_PUBLIC_BACKEND_URL` – the public URL of the FastAPI service (e.g. `https://api.example.com`).
- `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` – your Supabase project credentials.
- `SUPABASE_SERVICE_KEY_NONCE` & `SUPABASE_SERVICE_KEY_CIPHERTEXT` – encrypted service key values stored securely.
- `STRIPE_API_KEY` and `STRIPE_WEBHOOK_SECRET` – for billing and webhook verification.

## License

This project is provided as part of a learning exercise and comes without any warranty. Feel free to fork and adapt it for your own needs.
