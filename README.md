# Project: SideTap – Kotlin + FastAPI MVP

## 1. Frontend: Kotlin (Jetpack Compose)

- Use MVVM architecture
- Navigation Component for screen flow
- Retrofit or Ktor client for API calls
- Firebase Auth SDK (Google sign-in or email/pass)

## 2. Backend: FastAPI

### Endpoints
- POST /register
- POST /login
- GET /tasks
- POST /tasks
- GET /services
- POST /services
- POST /message (chat)
- POST /rate (optional MVP+)

### Libraries
- FastAPI
- SQLAlchemy + PostgreSQL or SQLite
- JWTAuth for token-based login
- Firebase Admin SDK (optional: use Firebase Auth for frontend only)

## 3. Realtime Chat Options
- Use Firebase Realtime DB for chat (simpler, low-latency)
- Or: Add WebSocket via FastAPI for self-hosted messaging (MVP++)

## 4. Deployment Suggestions
- Backend: Deploy on Railway, Fly.io, or Render (free tier usable)
- DB: PostgreSQL (Railway/Neon.tech)
- Media uploads: Firebase Storage or Cloudinary (for profile pics, etc.)
- Hosting App: Google Play Store (if you go public), internal APK for tests

## 5. Optional Tools
- Admin dashboard: Simple React or HTML panel with FastAPI backend
- CI/CD: GitHub Actions for backend deployment
- Monitoring: Sentry or LogRocket (optional)