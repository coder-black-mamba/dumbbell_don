### Dumbbell Don

Dumbbell Don is a comprehensive and robust gym management system designed to streamline operations for fitness centers. This powerful backend API is built with Django and Django REST Framework, providing a full suite of features to manage users, memberships, class schedules, payments, and more.

## Features

- **User Management**: Complete user system with roles for members, trainers, and staff.
- **Membership Plans**: Create and manage various membership plans.
- **Subscriptions**: Handle member subscriptions to different plans.
- **Class Scheduling**: Manage fitness class schedules and track member attendance.
- **Payment Processing**: Integrated payment system for handling invoices and transactions.
- **Feedback System**: Allow members to provide feedback on classes and services.
- **Reporting**: Generate reports for payments, attendance, and other key metrics.
- **API Documentation**: Self-documented API using Swagger (OpenAPI) and Redoc.

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: SQLite (for development)
- **Package Management**: uv
- **API Documentation**: drf-yasg (Swagger/Redoc)

## Project Setup

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Python 3.11
- `uv` package manager (`pip install uv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd dumbbell_don
    ```

2.  **Create a virtual environment and install dependencies:**
    This project uses `uv` for package management.
    ```bash
    uv venv
    uv sync
    ```
    This will create a `.venv` directory and install all the packages listed in `pyproject.toml`.

3.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Create a superuser:**
    This will allow you to access the Django admin panel.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## API Documentation

The API is fully documented using Swagger and Redoc. Once the server is running, you can access the documentation at the following endpoints:

-   **Swagger UI**: `http://127.0.0.1:8000/swagger/`
-   **Redoc**: `http://127.0.0.1:8000/redoc/`

## Running Tests

To run the automated tests for the project, use the following command:

```bash
python manage.py test
```

## Deployment

### Alhamdulillah Done On Time For Phitron