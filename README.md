# Veterinary Clinic Management System

### Installation

1. Clone the repository.
2. Install the required packages using poetry.

#### .env file example:
```bash
SECRET_KEY=your_secret_key
RECAPTCHA_PUBLIC_KEY=your_secret_key
RECAPTCHA_PRIVATE_KEY=your_secret_key
```

### Intructions to run the project

Make and apply migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

Collect static files:
```bash
python manage.py collectstatic
```

Create a superuser:
```bash
python manage.py createsuperuser
```

Run the server:
```bash
python manage.py runserver
```

#### Access the admin panel

http://127.0.0.1:8000/admin/
