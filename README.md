##  Django Auth Service

This is a Django project designed to provide authentication services with features for registration, login, and security
against suspicious requests. This project simulates a simple login/registration system similar to company’s current
process.

### User Stories - UseCases

- **User Registration:**
    - Enter phone number.
    - If the user is not registered:
        - A one-time 6-digit code is generated and sent via SMS.
        - User enters the verification code.
        - If the code is correct, the user is prompted to provide personal details (first name, last name, and email)
          and create a password.
        - If the code is incorrect, the user is notified.

- **User Login:**
    - Enter phone number and password.
    - If the user has registered before, they are authenticated upon correct password entry.
    - If the login credentials are incorrect:
        - After three failed attempts, either from the same IP or with the same username-password combination, the
          user/IP is blocked for 1 hour.

- **Security Measures:**
    - **Login Process:** After three incorrect attempts, the user or IP is blocked for 1 hour.
    - **Registration Process:** If three incorrect SMS verification codes are entered from the same IP or for the same
      phone number, the user/IP is blocked for 1 hour.

## Rate Limiting

Personal notes on rate limiting: I handle two approach of rate limiting in this project.

1. Rate limiting throughout hole project or service which is more efficient and clean.
2. Rate limiting throughout Actions (Login, Registration) which in there are too many unnecessary logics and codes. [(I have implemented this one on another branch)](https://github.com/MrRezoo/Django-Authentication-Service/tree/backup-main-different-rate-limiter-logic)

``` text
Besides the above notes,
1. I have implemented rate limiting in the service layer.
2. And I have implemented rate limiting in the middleware layer.
```

##### Middleware Layer

Middleware is a good place to implement a rate limiter since it can intercept requests before they reach the application
logic. This is beneficial because it ensures that requests exceeding the limit are blocked early in the request
lifecycle.
However, for more specific logic, such as blocking based on incorrect password attempts, service-level rate limiting may
be necessary.

##### Service Layer

Implement rate limiting in the authentication service where login and OTP requests are handled. This allows the rate
limiter to work in tandem with the business logic, such as checking the number of failed attempts and blocking the user
or IP if necessary.

##### Prerequisites

- Python 3.8+
- Poetry
- PostgreSQL

### Installation

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies:**
    ```sh
    poetry install
    ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following variables:
    ```env
    POSTGRES_NAME=<your-database-name>
    POSTGRES_USER=<your-database-user>
    POSTGRES_PASSWORD=<your-database-password>
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ALLOWED_HOSTS=*
    CSRF_TRUSTED_ORIGINS=<your-domain>
    ```

4. **Apply database migrations:**
    ```sh
    poetry run python src/manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    poetry run python src/manage.py createsuperuser
    ```

### Usage

- **Run the development server:**
    ```sh
    poetry run python src/manage.py runserver
    ```

- **Run tests:**
    ```sh
    poetry run python src/manage.py test
    ```

- **Run linters:**
    ```sh
    poetry run flake8 src/
    ```

### Makefile Commands

This project includes a `Makefile` for common tasks:

- `make install`: Install dependencies
- `make runserver`: Run the Django development server
- `make migrate`: Apply database migrations
- `make make-migration`: Create a migration
- `make dump-data`: Dump database data
- `make create-superuser`: Create a superuser
- `make db_shell`: Access the Django database shell
- `make shell`: Access the Django shell
- `make show-urls`: Display all project URLs
- `make test`: Run tests
- `make lint`: Run linters
- `make collect-static`: Collect static files
- `make make-messages`: Generate translation message files
- `make compile-messages`: Compile translation message files

### Project Structure

```
├── accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apis
│   │   ├── __init__.py
│   │   └── authentication.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers
│   │   ├── __init__.py
│   │   └── authentication.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── commands
│   │   │   ├── __init__.py
│   │   │   └── authentication.py
│   │   └── queries
│   │       ├── __init__.py
│   │       └── authentication.py
│   ├── tasks.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── authentication_apis_test.py
│   └── urls
│       ├── __init__.py
│       └── authentication.py
├── apis
│   ├── __init__.py
│   ├── accounts.py
│   └── urls.py
├── common
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── services
│   │   ├── __init__.py
│   │   └── rate_limiter
│   │       ├── __init__.py
│   │       ├── mixin.py
│   │       └── rate_limiter.py
│   ├── swagger.py
│   ├── throttles.py
│   ├── token_generator.py
│   ├── validators.py
│   ├── views.py
│   └── viewsets.py
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── env.py
│   ├── middlewares
│   │   ├── __init__.py
│   │   └── rate_limiter.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── django
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   ├── production.py
│   │   │   └── test.py
│   │   └── third_parties
│   │       ├── __init__.py
│   │       ├── caches.py
│   │       ├── cors.py
│   │       ├── drf.py
│   │       ├── jwt.py
│   │       ├── redis.py
│   │       ├── redis_templates.py
│   │       └── swagger.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
├── Makefile
├── .env
```

### License

This project is licensed under the MIT License.
