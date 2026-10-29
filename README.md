# WorkSphere HRMS — Phase 4

Phase 4 implementation for Employee Experience & System Integrations.

## Included Modules

- Module 21: Employee Onboarding System
- Module 22: Resignation & Exit Management
- Module 23: Internal Announcements System
- Module 24: Internal Task Assignment & Tracking
- Module 25: Third-Party Integrations
- Module 26: Employee Feedback System
- Module 27: Profile & Settings Management

## Technology Stack

- FastAPI
- SQLAlchemy 2
- SQLite by default
- JWT authentication
- Role-based authorization
- Pydantic validation
- CSV/PDF report exports
- Optional SMTP email integration

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies using `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Configure your environment variables and secret key.
5. Run the application:

   `uvicorn app.main:app --reload`

6. Open `http://127.0.0.1:8000/docs` to explore and test the API.

## Security

- JWT authentication
- Role-based access control
- Employee ownership validation
- Input validation
- Environment-based configuration

## Note

This Phase 4 implementation should be integrated with the existing WorkSphere Phases 1–3 database models and authentication system before deployment. Google Calendar synchronization requires additional OAuth configuration.
