# Authentication API Documentation

## Base URL
```
http://localhost:8000/backend/api/v1/auth
```

## Authentication Endpoints

### 1. User Login
**POST** `/login`

Login user with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "user@example.com",
      "type": "e"
    }
  }
}
```

### 2. Forgot Password
**POST** `/forgot-password`

Send password reset link to user's email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset link has been sent to your email."
}
```

### 3. Reset Password
**POST** `/reset-password`

Reset user password using reset token.

**Request Body:**
```json
{
  "token": "reset_token_here",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password has been reset successfully"
}
```

### 4. Email Verification
**POST** `/verify-email`

Verify user email using verification token.

**Request Body:**
```json
{
  "token": "verification_token_here"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email has been verified successfully"
}
```

### 5. Email Verification (GET)
**GET** `/verify-email?token=verification_token_here`

Verify user email using verification token (for email links).

**Response:**
```json
{
  "success": true,
  "message": "Email has been verified successfully"
}
```

### 6. Reset Password Form (GET)
**GET** `/reset-password?token=reset_token_here`

Get reset password form information (for email links).

**Response:**
```json
{
  "message": "Please use POST /reset-password with your token and new password",
  "token": "reset_token_here"
}
```

### 7. Change Password
**POST** `/change-password`

Change user password (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password has been changed successfully"
}
```

## User Registration Endpoint

### User Registration
**POST** `/users/register`

Register a new user account.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "type": "e",
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "user registration successfully",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "type": "e"
  }
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "success": false,
  "message": "Error description"
}
```

### Common Error Status Codes:
- **400**: Bad Request (invalid input data)
- **401**: Unauthorized (invalid credentials/token)
- **404**: Not Found (user not found)
- **409**: Conflict (email already exists)
- **500**: Internal Server Error

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Update `.env` file with your configuration:
```env
DB_URL = 'postgresql://postgres:your_password@localhost:5432/your_database'
JWT_SECRET = "your_jwt_secret_key"
JWT_ALGORITHM = "HS256"
BREVO_API_KEY = "your_brevo_api_key"
BREVO_SENDER_EMAIL = "noreply@yourdomain.com"
BREVO_SENDER_NAME = "Your App Name"
```

### 3. Database Migration
```bash
alembic upgrade head
```

### 4. Run the Application
```bash
uvicorn main:app --reload
```

## Features Implemented

- **User Registration** with email verification
- **User Login** with JWT token generation
- **Forgot Password** with email reset link
- **Reset Password** with token validation
- **Email Verification** flow
- **Change Password** (authenticated)
- **Brevo Email Service** integration
- **Password Hashing** with bcrypt
- **JWT Authentication** with token validation
- **Proper Error Handling** and validation
- **Email Templates** for verification and password reset

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Email verification tokens
- Password reset tokens with expiration
- Input validation and sanitization
- SQL injection prevention through SQLAlchemy ORM

## Email Templates

The application uses HTML email templates for:
- Email verification
- Password reset

Emails are sent using Brevo's SMTP API service.
