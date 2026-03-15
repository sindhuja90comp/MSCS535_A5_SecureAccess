# SecureAccess

SecureAccess is a Flask-based web application created for a cybersecurity assignment on secure database access. The project demonstrates how to expose a small user authentication system over HTTPS while protecting credentials in transit and reducing common database risks such as SQL injection.

## Project Overview

The application provides a simple registration and login workflow backed by SQLite. It is designed to show a safer approach to handling user input, password storage, and encrypted network communication in a small web service.

## Security Features

- HTTPS enabled server using a self-signed TLS certificate for local or classroom demonstration
- Automatic certificate and key generation when the app starts for the first time
- Parameterized SQL queries for user registration, login, and lookup
- Password hashing with Werkzeug before storing credentials in the database
- Basic username and password validation before database operations
- Rejection of invalid login attempts, including common SQL injection payloads

## Technology Stack

- Python 3
- Flask
- SQLite
- Werkzeug security helpers
- `cryptography` for certificate generation
- `requests` for the demo client and verification scripts

## Project Structure

- `app/` contains the Flask application, route handlers, database access, TLS support, and security logic
- `scripts/init_db.py` creates the SQLite database file and `users` table
- `scripts/demo_client.py` demonstrates registration, login, and a failed injection attempt
- `tests/test_security.py` performs a simple check against an injection-style login request
- `run.py` starts the HTTPS server

## How Secure Access Is Implemented

### 1. Protected database queries

Database operations use parameterized SQLite statements instead of building SQL strings from raw input. This prevents user-supplied values from being treated as executable SQL.

### 2. Secure password handling

Passwords are never stored in plain text. During registration, each password is hashed before being written to the database. During login, the submitted password is checked against the stored hash.

### 3. HTTPS communication

The application runs with TLS enabled, which encrypts traffic between the client and server. This helps protect login credentials from being exposed on the network during transmission.

### 4. Input validation

Usernames must match an allowed character pattern and passwords must meet minimum complexity requirements. This reduces malformed input and strengthens the login workflow.

## Setup and Execution

### 1. Create a virtual environment

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the database

```bash
python scripts/init_db.py
```

This creates `secure_app.db` with a `users` table.

### 4. Start the application

```bash
python run.py
```

The server starts on:

```text
https://127.0.0.1:5000
```

On first launch, the app generates `certs/server.crt` and `certs/server.key` automatically.

## Available Endpoints

### `GET /`

Returns a small JSON message showing that the HTTPS service is running.

### `POST /register`

Creates a new user account.

Example:

```bash
curl -k -X POST https://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"StrongPass123"}'
```

### `POST /login`

Authenticates a user with a username and password.

Example:

```bash
curl -k -X POST https://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"StrongPass123"}'
```

### `GET /user/<username>`

Fetches a user record by username without exposing the stored password hash.

Example:

```bash
curl -k https://127.0.0.1:5000/user/alice
```

## Demonstrating the Security Controls

Run the demo client after the server is running:

```bash
python scripts/demo_client.py
```

The script performs three actions:

- registers a user
- logs in with valid credentials
- sends an SQL injection-style login payload to show that authentication is denied

You can also run the verification script:

```bash
python tests/test_security.py
```

## Notes and Limitations

- The TLS certificate is self-signed, so clients such as `curl` use `-k` during local testing.
- SQLite is appropriate for a small classroom demo, but a production system would typically use a managed database and a production WSGI server.
- This project focuses on secure credential handling, encrypted transport, and safer query construction in a compact example.
