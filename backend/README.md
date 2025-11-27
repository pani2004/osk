# Python Email Backend Microservice

A Python implementation of the email backend service using FastAPI, replicating the functionality of the Node.js/Nodemailer backend.

## Features

- FastAPI web framework
- SMTP email sending using Python's smtplib
- Environment variable configuration
- Automatic API documentation at `/docs`
- Same API contract as the Node.js backend

## Requirements

- Python 3.8+
- Gmail account with app password

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Update the `.env` file with your actual Gmail credentials:
   - `EMAIL_USER`: Your Gmail address
   - `EMAIL_PASS`: Your Gmail app password (not regular password)
   - `EMAIL_TO`: Recipient email address
   - `PORT`: Port to run the server on (default: 8000)

## Running the Service

```bash
python main.py
```

The service will be available at `http://localhost:8000` (or your configured port).

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Usage

Send a POST request to `/api/contact` with the following JSON body:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Hello",
  "message": "This is a test message"
}
```

## Gmail App Password Setup

1. Enable 2-Factor Authentication on your Google Account
2. Go to Google Account settings
3. Navigate to Security → 2-Step Verification → App passwords
4. Generate a new app password for "Mail"
5. Use this app password as your `EMAIL_PASS` in the `.env` file