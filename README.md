# Faculty API

A FastAPI service that exposes endpoints for faculty search, resume upload, and compatibility scoring.

## Overview

This API provides a comprehensive solution for matching student resumes with faculty profiles based on research interests, education, and publications. It uses JWT-based authentication to secure endpoints.

## Features

- JWT-based authentication with user and admin roles
- Faculty search endpoint with filtering by keywords, university, department, and research areas
- Resume upload and parsing functionality
- Compatibility scoring between student resumes and faculty profiles
- RESTful API endpoints

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Python-jose (for JWT)
- Passlib (for password hashing)

## Installation

```bash
# Clone the repository
git clone https://github.com/Nikhil9989/faculty-api.git
cd faculty-api

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Accessible at http://localhost:8000/docs after starting the server. This provides a Swagger UI for interactive API testing.

## Authentication

- The API uses JWT tokens for authentication
- All endpoints (except token generation) require authentication
- Some endpoints are restricted to admin users

### Default Admin Credentials

- Email: admin@example.com
- Password: adminpassword

**Note:** Change these credentials in a production environment.

## License

MIT
