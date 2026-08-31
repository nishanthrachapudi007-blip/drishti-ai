# DrishtiAI

DrishtiAI is a production-oriented reference application for explainable diabetic-retinopathy screening workflows. It combines a polished React interface, a documented FastAPI contract, a PostgreSQL-ready schema, secure upload validation, and a replaceable inference service.

> **Medical disclaimer:** DrishtiAI is screening and decision-support software, not a definitive diagnosis or a replacement for a qualified eye-care professional. This repository ships without a trained or clinically validated model. Every current prediction is fixed demo content and must never be used for medical decisions.

## Architecture

- `frontend/`: responsive React 19 + TypeScript user experience, built with Vinext/Vite, Tailwind CSS, shadcn primitives, and Lucide icons
- `backend/`: FastAPI API, validation, SQLAlchemy data model, auth integration boundary, and screening orchestration
- `ml/`: model-integration contract and dataset safeguards
- `docs/`: architecture decisions
- `scripts/`: reserved for migration and operations helpers

The frontend and API deploy separately and communicate over HTTPS. PostgreSQL stores metadata, while production retinal images belong in private Supabase Storage or equivalent object storage. See [architecture](docs/architecture.md).

## Features

- Landing, login, signup, dashboard, upload, camera, processing, results, history, details, and settings views
- JPG/PNG type, decoded-image, and 10 MB size validation
- Five APTOS-style display classes: No DR, Mild NPDR, Moderate NPDR, Severe NPDR, and Proliferative DR
- Explicit demo labelling, plain-language explanations, risk guidance, and medical disclaimers
- Replaceable `InferenceService` boundary for a future PyTorch model
- PostgreSQL-ready users, screenings, images, predictions, explanations, and audit-history tables with relationships and indexes
- OpenAPI documentation, API tests, responsive design, camera fallback, and print-friendly results

## Local setup

Requirements: Node.js 22.13+, Python 3.12+, and optionally Docker for PostgreSQL.

1. Copy `.env.example` to `.env` and replace the development secrets.
2. Frontend: `cd frontend`, `npm install`, then `npm run dev`. Open `http://localhost:3000`.
3. Backend: create a virtual environment, install `backend/requirements.txt`, then run `uvicorn app.main:app --reload --app-dir backend`. Open `http://localhost:8000/docs` for the interactive API documentation.
4. Optional database: run `docker compose up db`. The current local demo service is intentionally in-memory; wire SQLAlchemy sessions and migrations before production.

## Environment variables

`NEXT_PUBLIC_API_URL` selects the public API origin. `DATABASE_URL`, `JWT_SECRET`, `ALLOWED_ORIGINS`, `MAX_UPLOAD_MB`, `INFERENCE_PROVIDER`, and `MODEL_PATH` configure the API. Supabase URL, service key, and bucket variables are reserved for server-side private storage. Never expose the service-role key to the browser.

## API

- `POST /auth/signup`, `POST /auth/login`
- `POST /screenings`
- `POST /screenings/{id}/image`
- `POST /screenings/{id}/analyze`
- `GET /screenings`, `GET /screenings/{id}`
- `GET /health`

The development auth endpoints return a conspicuously non-production token. Before launch, connect an OIDC/Supabase provider, verify signed access tokens in the API, and enforce per-user record ownership.

## Database and storage

The normalized schema is in `backend/app/models.py`. Use Alembic migrations in production. Keep images in a private storage bucket using random object keys and short-lived signed URLs; retain only the key, size, checksum, dimensions, and MIME type in PostgreSQL. Add consent, retention, deletion, and access-audit policies appropriate to your jurisdiction.

## ML service and datasets

The model layer is embedded behind `InferenceService`; it can later move to an independently scaled service without changing the public response contract. `DemoInferenceService` returns one fixed output solely to exercise the UI. Implement `TorchInferenceService` only after selecting a trained checkpoint and its exact preprocessing.

APTOS and mBRSET are not assumed to be interchangeable. Preserve the published label ontology, subject-level splits, licensing, provenance, and preprocessing for each dataset. Never infer labels from filenames or folder names and never create random image-to-label mappings.

For a real model: version and checksum the checkpoint, reproduce training preprocessing, validate image quality and retina presence, calibrate probabilities, evaluate sensitivity/specificity and subgroup performance on a held-out set, document thresholds, and clinically review Grad-CAM or the chosen explanation method.

## Testing

- Frontend: `npm run build` and `npm run lint` from `frontend/`
- Backend: `pytest backend/tests` from the repository root after installing requirements

The API test covers health, mandatory consent, validated upload, demo analysis, and its `is_demo` safety flag.

## Deployment

Deploy `frontend/` to a compatible Node/Cloudflare/Vite host and set `NEXT_PUBLIC_API_URL` to the HTTPS API. Build the backend container from `backend/Dockerfile`, attach managed PostgreSQL and private object storage, configure exact CORS origins, terminate TLS, run migrations, and keep secrets in the host's secret manager. Add rate limits, malware scanning, structured audit logs, backups, monitoring, and a data-processing agreement before accepting real health information.

The generated `.openai/hosting.json` allows the frontend to be deployed with OpenAI Sites, but no deployment was performed because repository handoff was requested for self-hosting.

## Limitations

The repository is a secure architectural starting point and a functional hackathon demonstration. It is not a medical device, has no regulatory clearance, provides no diagnostic accuracy claim, and includes no model checkpoint, dataset, production identity provider, persistence session wiring, or clinical validation.
