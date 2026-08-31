# Architecture

The browser app and API deploy independently. The frontend calls the FastAPI REST interface over HTTPS. FastAPI owns authentication enforcement, upload validation, screening orchestration, persistence, and the inference abstraction. PostgreSQL stores relational metadata; private object storage stores images and explanation artifacts. Production authentication should be delegated to Supabase Auth or another OIDC provider and verified by the API.

`Image → validated decode → documented preprocessing → InferenceService → calibrated probabilities → class → explainability service → API response → UI`

The in-memory demo API is intentionally limited to local demonstration. Production wiring must replace it with the included SQLAlchemy schema, migrations, private object storage, real token verification, and a trained/validated model.

