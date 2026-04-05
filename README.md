# Flow - Personal Finance Tracker

Flow is a Django-based personal finance app — a simplified reverse-engineering of a finance tool I actually use.
Originally built for the SoftUni Django Basics exam, then upgraded to a full Django Advanced project.

## Features

- **Dashboard** — financial summary, recent transactions, spending breakdown, active savings goals
- **Transaction management** — full CRUD for income and expense entries with category and tag support
- **Tag system** — create colour-coded labels and attach multiple tags per transaction
- **Category management** — organise spending with per-category budget limits and usage tracking
- **Savings goals** — set targets, track progress, attach related categories
- **User accounts** — register/login, per-user profile with currency preference and monthly budget limit
- **Profile pictures** — optional upload stored in `/media/profile_pictures/`
- **REST API** — JSON endpoints for transactions (list, create, retrieve, update, delete) using Django REST Framework
- **Budget alerts** — Celery task fires after every expense; sends an email if monthly spending exceeds 80% of the budget limit
- **Goal deadline reminders** — Celery Beat runs daily at 08:00 UTC; sends reminder emails for goals due within 7 days
- **Admin panel** — full model management via Django Admin
- **Responsive design** — Bootstrap 5

## Tech Stack

- Python / Django 4.2
- PostgreSQL
- Celery 5 + Redis (async tasks & scheduled jobs)
- Django REST Framework
- Pillow (image uploads)
- Bootstrap 5

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running (e.g. via Docker)
- Redis running (e.g. via Docker)

## Project Structure

```
Flow/
├── Flow/               # Django project config (settings, urls, celery)
├── api/                # DRF API app (transactions endpoints)
├── categories/         # Category model, views, templates
├── goals/              # SavingsGoal model, views, templates, Celery task
├── transactions/       # Transaction + Tag models, views, templates, Celery task
├── users/              # Custom profile, registration, login, profile views
├── templates/          # Global base/nav/footer/error templates
├── requirements.txt
└── manage.py
```

## Sample Data

Pre-loaded via migration seed files — no manual data entry needed to explore the app.
Includes 10 categories, 13 sample transactions, and 5 savings goals.
Seed data has no user attached; once you register and log in, your data is kept separate.
