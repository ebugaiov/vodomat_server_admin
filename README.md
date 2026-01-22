# Vodomat Server Admin

## Overview
Vodomat Server Admin is a Django-based web application designed for managing and administering the Vodomat Server system.

## Requirements
- Python >= 3.10.14
- Django >= 5.1.5
- MySQL >= 8.4
- Redis >= 5.2.1

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vodomat_server_admin
   ```
2. Install dependencies using uv:
   ```bash
   uv sync
   ```
3. Set up the database and environment variables.

## Running the Application
To run the application using uv, use the following command:
```bash
uv run python src/manage.py migrate
ur run python src/manage.py createsuperuser
uv run python src/manage.py runserver
```

## Docker Setup
To run the application using Docker, use the following command:
```bash
docker-compose up --build
```

## Acknowledgments
- Django framework
- MySQL database
- Docker for containerization
